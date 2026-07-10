"""
Campus Unlock — Specialization Model
=====================================
Represents a specialization within a category (e.g. Marketing,
Finance, HR, AI & ML, Cyber Security, Data Science).

Relationships:
- One Specialization belongs to one Category.
- One Specialization has many Programs.
"""

from datetime import datetime

from models import db


class Specialization(db.Model):
    __tablename__ = "specializations"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False
    )
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    category = db.relationship(
        "Category",
        back_populates="specializations",
    )
    programs = db.relationship(
        "Program",
        back_populates="specialization",
        lazy=True,
    )

    def __repr__(self):
        return f"<Specialization id={self.id} name={self.name!r}>"
