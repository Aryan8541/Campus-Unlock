"""
Campus Unlock — PlacementPartner Model
========================================
Represents a company that recruits students from a university,
displayed on the university's placement section.

Relationships
-------------
- Many PlacementPartners belong to one University.
"""

from datetime import datetime

from models import db


class PlacementPartner(db.Model):
    __tablename__ = "placement_partners"

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
    company_name = db.Column(db.String(200), nullable=False)

    # URL of the recruiter's logo; None if not yet uploaded.
    logo_url     = db.Column(db.String(500), nullable=True)

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
        back_populates="placement_partners",
    )

    def __repr__(self):
        return f"<PlacementPartner id={self.id} company={self.company_name!r} university_id={self.university_id}>"
