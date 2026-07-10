"""
Campus Unlock — Program Model
===============================
Represents a specific degree program offered by a university, under
a given category and specialization.

Relationships:
- Many Programs belong to one University.
- Many Programs belong to one Category.
- Many Programs belong to one Specialization.
"""

from datetime import datetime

from models import db


class Program(db.Model):
    __tablename__ = "programs"

    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(
        db.Integer, db.ForeignKey("universities.id"), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False
    )
    specialization_id = db.Column(
        db.Integer, db.ForeignKey("specializations.id"), nullable=True
    )

    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), nullable=False, unique=True, index=True)
    duration = db.Column(db.String(100), nullable=True)
    fees = db.Column(db.Numeric(12, 2), nullable=True)
    eligibility = db.Column(db.Text, nullable=True)
    mode = db.Column(db.String(50), nullable=True)
    brochure = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
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
        back_populates="programs",
    )
    category = db.relationship(
        "Category",
        back_populates="programs",
    )
    specialization = db.relationship(
        "Specialization",
        back_populates="programs",
    )

    def __repr__(self):
        return f"<Program id={self.id} title={self.title!r}>"
