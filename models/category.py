"""
Campus Unlock — Category Model
===============================
Represents a top-level program category (e.g. MBA, MCA, BCA, BBA,
B.Tech, M.Tech).

Relationships:
- One Category has many Specializations.
- One Category has many Programs.
"""

from datetime import datetime

from models import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    specializations = db.relationship(
        "Specialization",
        back_populates="category",
        lazy=True,
        cascade="all, delete-orphan",
    )
    programs = db.relationship(
        "Program",
        back_populates="category",
        lazy=True,
    )

    def __repr__(self):
        return f"<Category id={self.id} name={self.name!r}>"
