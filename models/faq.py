"""
Campus Unlock — FAQ Model
==========================
Represents a Frequently Asked Question associated with a university.

Relationships
-------------
- Many FAQs belong to one University.
"""

from datetime import datetime

from models import db


class FAQ(db.Model):
    __tablename__ = "faqs"

    # ------------------------------------------------------------------
    # Primary key
    # ------------------------------------------------------------------
    id = db.Column(db.Integer, primary_key=True)

    # ------------------------------------------------------------------
    # Foreign key
    # ------------------------------------------------------------------
    university_id = db.Column(
        db.Integer,
        db.ForeignKey("universities.id"),
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------
    # Core fields
    # ------------------------------------------------------------------
    question = db.Column(db.String(500), nullable=False)
    answer   = db.Column(db.Text,        nullable=False)

    # Display order within a university's FAQ list (lower = first).
    # Default None means order is unspecified; consumers should sort
    # by (sort_order NULLS LAST, id ASC) for a stable sequence.
    sort_order = db.Column(db.Integer, nullable=True)

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------
    is_active  = db.Column(db.Boolean,  nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    university = db.relationship(
        "University",
        back_populates="faqs",
    )

    def __repr__(self):
        return f"<FAQ id={self.id} university_id={self.university_id} question={self.question[:40]!r}>"
