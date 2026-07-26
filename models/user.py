"""
Campus Unlock — User Model
===========================
Represents a platform user account. Password storage uses Werkzeug's
salted hashing (generate_password_hash / check_password_hash) — the
plain-text password is never persisted.

No authentication routes, sessions, or login logic are implemented
here; this is the model definition only.
"""

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from models import db

# Known role values for `User.role`. Not a DB constraint (the column is a
# plain string so new roles never need a migration) — this is just the
# single place that lists what currently exists, kept in step with
# ROLE_DASHBOARD_ENDPOINTS in routes/main.py. Adding a role (e.g.
# "counselor") means adding it here, adding its dashboard route + a
# ROLE_DASHBOARD_ENDPOINTS entry, and nothing else.
ROLE_STUDENT = "student"
ROLE_TEACHER = "teacher"
ROLE_ADMIN = "admin"
KNOWN_ROLES = (ROLE_STUDENT, ROLE_TEACHER, ROLE_ADMIN)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True, index=True)
    mobile = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # ------------------------------------------------------------------
    # Phase 8A — Role-based authentication (Admin System foundation)
    # ------------------------------------------------------------------
    # Additive column. `is_admin` above is left untouched for backward
    # compatibility with any existing code paths that still read it;
    # `role` is the new source of truth for authorization decisions
    # going forward (admin_required, login redirects, navbar).
    role = db.Column(
        db.String(20),
        nullable=False,
        default="student",
        server_default="student",
    )
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ------------------------------------------------------------------
    # Password handling
    # ------------------------------------------------------------------
    def set_password(self, raw_password):
        """Hash and store the given plain-text password."""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """Verify a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, raw_password)

    # ------------------------------------------------------------------
    # Phase 8A — Role helpers
    # ------------------------------------------------------------------
    def is_admin_role(self):
        """True if this user's role is 'admin'. Used by admin_required
        and login()'s post-auth redirect; does not read/alter is_admin."""
        return self.role == "admin"

    def __repr__(self):
        return f"<User id={self.id} email={self.email!r}>"
