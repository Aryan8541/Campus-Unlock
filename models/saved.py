"""
Campus Unlock — Saved Items Models (Phase 7C-1)
================================================
Two lightweight join tables that let authenticated users bookmark
universities and programs.  Deliberately kept separate from the Lead /
enquiry flow — saving is a soft "wishlist" action, not a commitment.

Relationships
-------------
SavedUniversity  →  User        (FK: users.id,        cascade delete)
SavedUniversity  →  University  (FK: universities.id, cascade delete)

SavedProgram     →  User        (FK: users.id,        cascade delete)
SavedProgram     →  Program     (FK: programs.id,     cascade delete)

Unique constraints prevent duplicate rows per (user, item) pair so the
toggle endpoints can rely on a simple "row exists?" check rather than
counting rows.
"""

from datetime import datetime

from models import db


class SavedUniversity(db.Model):
    __tablename__ = "saved_universities"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    university_id = db.Column(
        db.Integer,
        db.ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Prevent duplicate saves
    __table_args__ = (
        db.UniqueConstraint("user_id", "university_id", name="uq_saved_university"),
    )

    # Relationships — lazy="joined" so the university/user are loaded in the
    # same query when we fetch a user's saved list (avoids N+1).
    user = db.relationship("User", backref=db.backref("saved_universities", lazy="dynamic"))
    university = db.relationship(
        "University",
        backref=db.backref("saved_by_users", lazy="dynamic"),
        lazy="joined",
    )

    def __repr__(self):
        return f"<SavedUniversity user={self.user_id} uni={self.university_id}>"


class SavedProgram(db.Model):
    __tablename__ = "saved_programs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    program_id = db.Column(
        db.Integer,
        db.ForeignKey("programs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Prevent duplicate saves
    __table_args__ = (
        db.UniqueConstraint("user_id", "program_id", name="uq_saved_program"),
    )

    user = db.relationship("User", backref=db.backref("saved_programs", lazy="dynamic"))
    program = db.relationship(
        "Program",
        backref=db.backref("saved_by_users", lazy="dynamic"),
        lazy="joined",
    )

    def __repr__(self):
        return f"<SavedProgram user={self.user_id} prog={self.program_id}>"
