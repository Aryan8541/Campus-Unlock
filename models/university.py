"""
Campus Unlock — University Model
==================================
Represents a university/institution listed on the platform.

Relationships:
- One University has many Programs.
"""

from datetime import datetime

from models import db


class University(db.Model):
    __tablename__ = "universities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), nullable=False, unique=True, index=True)
    logo = db.Column(db.String(255), nullable=True)
    banner = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    accreditation = db.Column(db.String(200), nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    established_year = db.Column(db.Integer, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(120), nullable=True)
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
    programs = db.relationship(
        "Program",
        back_populates="university",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<University id={self.id} name={self.name!r}>"
