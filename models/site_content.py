"""
Campus Unlock — SiteContent Model (Phase 9: CMS & Content)
============================================================
A simple key/value store for homepage content and site-wide SEO that
doesn't belong to any single University or Program — the kind of thing
that used to require editing seed.py by hand.

Deliberately key/value rather than one column per field: new homepage
sections (a new stat, a new SEO field) can be added from the admin UI
without a schema migration. Consumers look up a key via SiteContent.get()
and fall back to a sane default when the row doesn't exist yet (e.g. on
a fresh DB before an admin has edited anything).

Known keys currently in use (see routes/admin.py SITE_CONTENT_FIELDS
and routes/main.py index()):
  stat_students        — homepage "Students guided" number (e.g. "50000")
  stat_universities     — homepage "Verified universities" number
  stat_admission_pct    — homepage "Admission support" percentage
  homepage_seo_title       — <title> override for "/"
  homepage_seo_description — meta description override for "/"
"""

from datetime import datetime

from models import db


class SiteContent(db.Model):
    __tablename__ = "site_content"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False, unique=True, index=True)
    value = db.Column(db.Text, nullable=True)

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"<SiteContent key={self.key!r}>"

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    @staticmethod
    def get(key, default=None):
        """Fetch a single value by key, or `default` if unset."""
        row = SiteContent.query.filter_by(key=key).first()
        return row.value if row and row.value is not None else default

    @staticmethod
    def get_many(keys):
        """Fetch several keys at once as a {key: value} dict. Keys not
        present in the DB are simply absent from the returned dict —
        callers should apply their own defaults."""
        rows = SiteContent.query.filter(SiteContent.key.in_(keys)).all()
        return {row.key: row.value for row in rows}

    @staticmethod
    def set(key, value):
        """Create or update a single key's value."""
        row = SiteContent.query.filter_by(key=key).first()
        if row is None:
            row = SiteContent(key=key, value=value)
            db.session.add(row)
        else:
            row.value = value
            row.updated_at = datetime.utcnow()
        return row
