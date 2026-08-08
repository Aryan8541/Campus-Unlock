"""
Campus Unlock — Password Reset Token Model
==========================================
Stores a *hashed* reset token so the raw token only ever exists in the
reset-link URL and in the user's email client — never in the database.

Security design
---------------
- The raw token (secrets.token_urlsafe(32)) is generated in the route,
  sent in the email, and immediately discarded from memory after hashing.
- Only the SHA-256 hash of the token is persisted here (token_hash).
- The route receives the raw token from the URL, hashes it, and compares
  the hash — the raw token is never written to logs or the DB.
- Tokens expire after RESET_TOKEN_EXPIRY_MINUTES (default 30).
- Tokens are single-use: used_at is set on first successful reset; any
  subsequent attempt that finds used_at IS NOT NULL is rejected.
- A simple per-email cooldown (last_sent_at) prevents unlimited reset
  spam without requiring a new dependency.
"""

from datetime import datetime

from models import db


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)

    # FK to the user who requested the reset.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # SHA-256 hex digest of the raw URL token. The raw token is never stored.
    token_hash = db.Column(db.String(64), nullable=False, unique=True, index=True)

    # Expiry — checked on every use attempt.
    expires_at = db.Column(db.DateTime, nullable=False)

    # Set when the token is successfully consumed; prevents reuse.
    used_at = db.Column(db.DateTime, nullable=True, default=None)

    # Audit / rate-limit reference.
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship back to User (read-only convenience; no cascade needed
    # because the FK already has ondelete="CASCADE").
    user = db.relationship("User", backref=db.backref("reset_tokens", lazy=True))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @property
    def is_expired(self):
        """True if the token's expiry timestamp has passed."""
        return datetime.utcnow() > self.expires_at

    @property
    def is_used(self):
        """True if the token has already been consumed."""
        return self.used_at is not None

    @property
    def is_valid(self):
        """True only when the token is both unused and not expired."""
        return not self.is_used and not self.is_expired

    def mark_used(self):
        """Stamp used_at; caller must db.session.commit()."""
        self.used_at = datetime.utcnow()

    def __repr__(self):
        return (
            f"<PasswordResetToken id={self.id} user_id={self.user_id} "
            f"valid={self.is_valid!r}>"
        )
