"""
Campus Unlock — University Model
==================================
Represents a university/institution listed on the platform.

Relationships
-------------
- One University has many Programs          (cascade delete)
- One University has many Scholarships      (cascade delete)
- One University has many FAQs              (cascade delete)
- One University has many PlacementPartners (cascade delete)

Fields added in this revision
------------------------------
Branding
    logo_url, banner_url, brochure_url

University Information
    short_description, full_description, why_choose,
    established_year, ownership, university_type

Recognition / Approvals
    ugc_approved, aicte_approved, aiu_member, wes_approved

Placement
    placement_support, highest_package, average_package, top_recruiters

Statistics
    total_students, faculty_count, alumni_count

Contact
    email, phone, address

SEO
    meta_title, meta_description

Media
    gallery_images  — JSON array stored as Text; use json.loads() to read

Note: the original `logo`, `banner`, and `description` columns are
retained unchanged so existing routes/templates/seed data continue to
work without any migration on those columns.  The new *_url fields and
*_description fields are the authoritative production equivalents and
can be populated going forward.
"""

from datetime import datetime

from models import db


class University(db.Model):
    __tablename__ = "universities"

    # ------------------------------------------------------------------
    # Primary key
    # ------------------------------------------------------------------
    id = db.Column(db.Integer, primary_key=True)

    # ------------------------------------------------------------------
    # Core identity (unchanged from original)
    # ------------------------------------------------------------------
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), nullable=False, unique=True, index=True)

    # ------------------------------------------------------------------
    # Branding
    # Original columns kept for backwards-compatibility with seed / routes.
    # New *_url columns are the production-ready equivalents.
    # ------------------------------------------------------------------
    logo        = db.Column(db.String(255), nullable=True)   # legacy — kept
    banner      = db.Column(db.String(255), nullable=True)   # legacy — kept
    logo_url    = db.Column(db.String(500), nullable=True)
    banner_url  = db.Column(db.String(500), nullable=True)
    brochure_url = db.Column(db.String(500), nullable=True)

    # ------------------------------------------------------------------
    # University information
    # `description` kept for backwards-compatibility with seed / routes.
    # ------------------------------------------------------------------
    description       = db.Column(db.Text, nullable=True)    # legacy — kept
    short_description = db.Column(db.String(500), nullable=True)
    full_description  = db.Column(db.Text, nullable=True)
    why_choose        = db.Column(db.Text, nullable=True)   # "Why choose us" copy

    established_year  = db.Column(db.Integer, nullable=True)
    ownership         = db.Column(db.String(50),  nullable=True)   # e.g. "Private", "Government", "Deemed"
    university_type   = db.Column(db.String(100), nullable=True)   # e.g. "Deemed-to-be University", "State University"

    # ------------------------------------------------------------------
    # Accreditation / recognition (original field kept)
    # ------------------------------------------------------------------
    accreditation = db.Column(db.String(200), nullable=True)   # legacy — kept (NAAC grade string)
    ranking       = db.Column(db.Integer,     nullable=True)   # NIRF rank — legacy, kept

    ugc_approved  = db.Column(db.Boolean, nullable=False, default=False)
    aicte_approved = db.Column(db.Boolean, nullable=False, default=False)
    aiu_member    = db.Column(db.Boolean, nullable=False, default=False)
    wes_approved  = db.Column(db.Boolean, nullable=False, default=False)

    # ------------------------------------------------------------------
    # Placement
    # ------------------------------------------------------------------
    placement_support  = db.Column(db.Boolean, nullable=False, default=False)
    highest_package    = db.Column(db.Numeric(12, 2), nullable=True)   # annual CTC in INR
    average_package    = db.Column(db.Numeric(12, 2), nullable=True)   # annual CTC in INR
    top_recruiters     = db.Column(db.Text, nullable=True)             # comma-separated or plain-text list

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------
    total_students = db.Column(db.Integer, nullable=True)
    faculty_count  = db.Column(db.Integer, nullable=True)
    alumni_count   = db.Column(db.Integer, nullable=True)

    # ------------------------------------------------------------------
    # Contact
    # ------------------------------------------------------------------
    email   = db.Column(db.String(254), nullable=True)
    phone   = db.Column(db.String(20),  nullable=True)
    address = db.Column(db.Text,        nullable=True)

    # Original location columns — kept unchanged
    city    = db.Column(db.String(120), nullable=True)
    state   = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(255), nullable=True)

    # ------------------------------------------------------------------
    # SEO
    # ------------------------------------------------------------------
    meta_title       = db.Column(db.String(160), nullable=True)
    meta_description = db.Column(db.String(320), nullable=True)

    # ------------------------------------------------------------------
    # Media
    # Stored as a JSON-encoded text string, e.g.:
    #   '["https://cdn.example.com/img1.jpg", "https://cdn.example.com/img2.jpg"]'
    # Use json.loads(university.gallery_images or "[]") to consume.
    # ------------------------------------------------------------------
    gallery_images = db.Column(db.Text, nullable=True)

    # ------------------------------------------------------------------
    # Status / audit (unchanged)
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
    programs = db.relationship(
        "Program",
        back_populates="university",
        lazy=True,
        cascade="all, delete-orphan",
    )

    scholarships = db.relationship(
        "Scholarship",
        back_populates="university",
        lazy=True,
        cascade="all, delete-orphan",
    )

    faqs = db.relationship(
        "FAQ",
        back_populates="university",
        lazy=True,
        cascade="all, delete-orphan",
    )

    placement_partners = db.relationship(
        "PlacementPartner",
        back_populates="university",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<University id={self.id} name={self.name!r}>"
