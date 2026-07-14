"""
Campus Unlock — User History Models (Phase 7C-2)
=================================================
Three lightweight event tables that capture per-user browsing and
interaction history.  All are append-only from the application's
perspective; the only deletion path is the explicit "Clear History"
action available on the dashboard.

Tables
------
recently_viewed
    One row per visit to a University or Program detail page.
    Duplicates are collapsed by DELETE + INSERT in the route so the
    list always reflects the 10 most-recently-visited distinct items,
    newest first.

compare_history
    One row per "Compare" action; stores the ordered list of
    university IDs as a comma-separated string so no join table is
    needed for a UI-only history feature.

brochure_downloads
    One row per brochure link click, linked to either a University or
    a Program (or both — the PDF may be the university brochure served
    from a program page).

Design choices
--------------
* No UniqueConstraint on recently_viewed — ORDER BY + LIMIT handles
  deduplication in the route (simpler than a partial index on SQLite).
* CompareHistory stores university_ids as TEXT — the list is always
  presented together as a snapshot; no FK integrity is needed.
* All tables CASCADE DELETE on user_id so wiping a user account also
  wipes their history without application code.
"""

from datetime import datetime

from models import db


class RecentlyViewed(db.Model):
    __tablename__ = "recently_viewed"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Exactly one of these is populated per row.
    university_id = db.Column(
        db.Integer,
        db.ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    program_id = db.Column(
        db.Integer,
        db.ForeignKey("programs.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    viewed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Relationships — lazy="joined" so the related object is loaded in the
    # same query that fetches the history list (no N+1 on the dashboard).
    university = db.relationship(
        "University",
        backref=db.backref("recently_viewed_by", lazy="dynamic"),
        lazy="joined",
        foreign_keys=[university_id],
    )
    program = db.relationship(
        "Program",
        backref=db.backref("recently_viewed_by", lazy="dynamic"),
        lazy="joined",
        foreign_keys=[program_id],
    )

    def __repr__(self):
        target = f"uni={self.university_id}" if self.university_id else f"prog={self.program_id}"
        return f"<RecentlyViewed user={self.user_id} {target}>"


class CompareHistory(db.Model):
    __tablename__ = "compare_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Comma-separated university IDs in the order the user selected them,
    # e.g. "3,7,12".  Stored as text — this is display-only history, not
    # a relational dependency that needs FK enforcement.
    university_ids = db.Column(db.String(100), nullable=False)
    # Human-readable names snapshot so the dashboard can display them even
    # if a university is later renamed or deactivated.
    university_names = db.Column(db.Text, nullable=True)
    compared_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<CompareHistory user={self.user_id} ids={self.university_ids!r}>"

    @property
    def id_list(self):
        """Return university_ids as a Python list of strings."""
        return [x.strip() for x in (self.university_ids or "").split(",") if x.strip()]

    @property
    def name_list(self):
        """Return university_names as a Python list of strings."""
        return [x.strip() for x in (self.university_names or "").split(",") if x.strip()]


class BrochureDownload(db.Model):
    __tablename__ = "brochure_downloads"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # At least one of university_id / program_id will be set.
    university_id = db.Column(
        db.Integer,
        db.ForeignKey("universities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    program_id = db.Column(
        db.Integer,
        db.ForeignKey("programs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    downloaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    university = db.relationship(
        "University",
        backref=db.backref("brochure_downloads", lazy="dynamic"),
        lazy="joined",
        foreign_keys=[university_id],
    )
    program = db.relationship(
        "Program",
        backref=db.backref("brochure_downloads", lazy="dynamic"),
        lazy="joined",
        foreign_keys=[program_id],
    )

    def __repr__(self):
        return f"<BrochureDownload user={self.user_id} uni={self.university_id} prog={self.program_id}>"
