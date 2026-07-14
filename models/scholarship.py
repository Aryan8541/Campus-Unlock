"""
Campus Unlock — Scholarship Model
===================================
Represents a scholarship offered by a university.

Relationships
-------------
- Many Scholarships belong to one University.
"""

from datetime import datetime

from models import db


class Scholarship(db.Model):
    __tablename__ = "scholarships"

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
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        nullable=True)

    # Amount in INR; None means the value is variable / on-request.
    amount      = db.Column(db.Numeric(12, 2), nullable=True)

    # ISO-8601 date string stored as Text (e.g. "2025-12-31") so it
    # remains human-readable in SQLite without a date type.
    # Use datetime.strptime(university.scholarships[0].deadline, "%Y-%m-%d")
    # to parse when needed.
    deadline    = db.Column(db.String(20), nullable=True)

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
        back_populates="scholarships",
    )

    def __repr__(self):
        return f"<Scholarship id={self.id} title={self.title!r} university_id={self.university_id}>"
