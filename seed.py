"""
Campus Unlock — Database Seed Script
======================================
Populates the database with realistic demo data:
  - 6 Categories
  - 8 Specializations
  - 10 Universities
  - 25+ Programs (linked to University + Category + Specialization)
  - 5 Leads
  - 3 Users (with hashed passwords via the existing User model)

Safe to run multiple times: every insert is guarded by an existence
check on a natural unique key (slug / email), so re-running this
script will not create duplicate rows. All work happens in a single
SQLAlchemy session and is committed exactly once at the end; any
failure triggers a full rollback.

Usage:
    python seed.py
"""

import os
import re
import sys
from datetime import datetime, timedelta

from app import create_app
from config import config as config_map
from models import db, Category, Specialization, University, Program, User, Lead


def slugify(text):
    """Lowercase, hyphen-separated slug from an arbitrary string."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug


# ----------------------------------------------------------------------
# Generic idempotent get-or-create helper
# ----------------------------------------------------------------------
def get_or_create(model, lookup, defaults=None):
    """
    Return an existing row matching `lookup` (a dict of unique-key
    filters), or build a new (unsaved, session-added) instance using
    `lookup` + `defaults`. Never issues a commit.
    """
    instance = model.query.filter_by(**lookup).first()
    if instance:
        return instance, False

    params = dict(lookup)
    if defaults:
        params.update(defaults)
    instance = model(**params)
    db.session.add(instance)
    return instance, True


# ----------------------------------------------------------------------
# Seed data definitions
# ----------------------------------------------------------------------
CATEGORY_NAMES = ["MBA", "MCA", "BCA", "BBA", "B.Tech", "M.Tech"]

SPECIALIZATION_DEFS = [
    # (name, home category name)
    ("Marketing", "MBA"),
    ("Finance", "MBA"),
    ("HR", "MBA"),
    ("AI & ML", "M.Tech"),
    ("Cyber Security", "MCA"),
    ("Data Science", "M.Tech"),
    ("Cloud Computing", "MCA"),
    ("Software Engineering", "B.Tech"),
]

UNIVERSITY_DEFS = [
    {
        "name": "Amity University Online",
        "city": "Noida",
        "state": "Uttar Pradesh",
        "website": "https://online.amity.edu",
        "ranking": 12,
        "accreditation": "NAAC A+",
        "established_year": 2005,
        "description": "One of India's largest private universities, offering UGC-DEB approved online degrees across management, IT, and commerce.",
    },
    {
        "name": "NMIMS Global Access",
        "city": "Mumbai",
        "state": "Maharashtra",
        "website": "https://online.nmims.edu",
        "ranking": 8,
        "accreditation": "NAAC A+",
        "established_year": 2007,
        "description": "NMIMS' distance and online learning arm, known for its strong online MBA and finance-focused programs.",
    },
    {
        "name": "Manipal University Jaipur Online",
        "city": "Jaipur",
        "state": "Rajasthan",
        "website": "https://online.manipaljaipur.edu.in",
        "ranking": 25,
        "accreditation": "NAAC A",
        "established_year": 2011,
        "description": "Part of the Manipal Education Group, offering flexible online degrees in management and technology.",
    },
    {
        "name": "Lovely Professional University Online",
        "city": "Phagwara",
        "state": "Punjab",
        "website": "https://online.lpu.in",
        "ranking": 18,
        "accreditation": "NAAC A++",
        "established_year": 2012,
        "description": "LPU's online division, offering a wide catalogue of UGC-approved undergraduate and postgraduate programs.",
    },
    {
        "name": "Jain Online (Deemed-to-be University)",
        "city": "Bengaluru",
        "state": "Karnataka",
        "website": "https://www.jainonline.ac.in",
        "ranking": 20,
        "accreditation": "NAAC A++",
        "established_year": 2010,
        "description": "Jain University's online platform, popular for tech-focused BCA/MCA and business programs.",
    },
    {
        "name": "Chandigarh University Online",
        "city": "Mohali",
        "state": "Punjab",
        "website": "https://online.cuchd.in",
        "ranking": 30,
        "accreditation": "NAAC A+",
        "established_year": 2013,
        "description": "A fast-growing online education provider with strong placement tie-ups in IT and management.",
    },
    {
        "name": "Dr. D. Y. Patil Vidyapeeth Online",
        "city": "Pune",
        "state": "Maharashtra",
        "website": "https://online.dpu.edu.in",
        "ranking": 35,
        "accreditation": "NAAC A",
        "established_year": 2014,
        "description": "Known for healthcare-adjacent management programs alongside core online MBA and BBA offerings.",
    },
    {
        "name": "Sikkim Manipal University Distance Education",
        "city": "Gangtok",
        "state": "Sikkim",
        "website": "https://online.smude.edu.in",
        "ranking": 40,
        "accreditation": "NAAC A",
        "established_year": 2001,
        "description": "One of the earliest UGC-DEB recognised distance and online education providers in India.",
    },
    {
        "name": "Shoolini University Online",
        "city": "Solan",
        "state": "Himachal Pradesh",
        "website": "https://online.shooliniuniversity.com",
        "ranking": 45,
        "accreditation": "NAAC A+",
        "established_year": 2015,
        "description": "A research-focused university expanding into online management and computer application degrees.",
    },
    {
        "name": "Vivekananda Global University Online",
        "city": "Jaipur",
        "state": "Rajasthan",
        "website": "https://online.vgu.ac.in",
        "ranking": 55,
        "accreditation": "NAAC B++",
        "established_year": 2012,
        "description": "An affordable UGC-DEB approved option for working professionals across Rajasthan and beyond.",
    },
]

# Each entry: (university_name, category_name, specialization_name_or_None,
#              title, duration, fees, eligibility, mode)
PROGRAM_DEFS = [
    ("Amity University Online", "MBA", "Marketing", "Online MBA - Marketing", "2 Years", 150000, "Graduation in any discipline with 50% marks", "Online"),
    ("Amity University Online", "MCA", "Cyber Security", "Online MCA - Cyber Security", "2 Years", 120000, "Bachelor's degree with Mathematics at 10+2 or graduation level", "Online"),
    ("Amity University Online", "BBA", None, "Online BBA", "3 Years", 90000, "10+2 in any stream from a recognised board", "Online"),

    ("NMIMS Global Access", "MBA", "Finance", "Online MBA - Finance", "2 Years", 175000, "Graduation with 50% aggregate marks", "Online"),
    ("NMIMS Global Access", "BCA", None, "Online BCA", "3 Years", 85000, "10+2 with Mathematics as a subject", "Online"),
    ("NMIMS Global Access", "M.Tech", "AI & ML", "Online M.Tech - AI & ML", "2 Years", 140000, "B.Tech/B.E. or equivalent with 50% marks", "Online"),

    ("Manipal University Jaipur Online", "MBA", "HR", "Online MBA - HR", "2 Years", 130000, "Graduation in any discipline with 50% marks", "Online"),
    ("Manipal University Jaipur Online", "MCA", "Cloud Computing", "Online MCA - Cloud Computing", "2 Years", 110000, "Bachelor's degree with Mathematics/Computer Science", "Online"),
    ("Manipal University Jaipur Online", "BBA", None, "Online BBA - General Management", "3 Years", 95000, "10+2 in any stream", "Online"),

    ("Lovely Professional University Online", "MBA", "Marketing", "Online MBA - Marketing & Sales", "2 Years", 128000, "Graduation with 50% marks", "Online"),
    ("Lovely Professional University Online", "BCA", None, "Online BCA", "3 Years", 78000, "10+2 with Mathematics", "Online"),
    ("Lovely Professional University Online", "B.Tech", "Software Engineering", "Online B.Tech - Software Engineering (Lateral)", "3 Years", 165000, "Diploma in Engineering or 10+2 with PCM", "Online"),

    ("Jain Online (Deemed-to-be University)", "BCA", None, "Online BCA - Software Development", "3 Years", 82000, "10+2 with Mathematics as a subject", "Online"),
    ("Jain Online (Deemed-to-be University)", "MCA", "Cloud Computing", "Online MCA - Cloud Computing & Data Science", "2 Years", 115000, "Bachelor's degree in a relevant discipline", "Online"),
    ("Jain Online (Deemed-to-be University)", "MBA", "Finance", "Online MBA - Banking & Finance", "2 Years", 145000, "Graduation with 50% marks", "Online"),

    ("Chandigarh University Online", "MBA", "HR", "Online MBA - Human Resource Management", "2 Years", 120000, "Graduation in any discipline", "Online"),
    ("Chandigarh University Online", "BBA", None, "Online BBA - Digital Business", "3 Years", 88000, "10+2 in any stream", "Online"),
    ("Chandigarh University Online", "M.Tech", "Data Science", "Online M.Tech - Data Science", "2 Years", 138000, "B.Tech/B.E. or MCA with 50% marks", "Online"),

    ("Dr. D. Y. Patil Vidyapeeth Online", "MBA", "Marketing", "Online MBA - Marketing Management", "2 Years", 135000, "Graduation with 50% aggregate marks", "Online"),
    ("Dr. D. Y. Patil Vidyapeeth Online", "BBA", None, "Online BBA - Healthcare Management", "3 Years", 92000, "10+2 in any stream", "Online"),

    ("Sikkim Manipal University Distance Education", "MCA", "Cyber Security", "Online MCA - Information Security", "2 Years", 105000, "Bachelor's degree with Mathematics/Computer Science", "Online"),
    ("Sikkim Manipal University Distance Education", "BCA", None, "Online BCA - General", "3 Years", 70000, "10+2 with Mathematics", "Online"),
    ("Sikkim Manipal University Distance Education", "MBA", "Finance", "Online MBA - Financial Management", "2 Years", 118000, "Graduation with 50% marks", "Online"),

    ("Shoolini University Online", "M.Tech", "AI & ML", "Online M.Tech - Artificial Intelligence", "2 Years", 148000, "B.Tech/B.E. with 55% marks", "Online"),
    ("Shoolini University Online", "MBA", "HR", "Online MBA - HR & Organisational Behaviour", "2 Years", 125000, "Graduation in any discipline", "Online"),

    ("Vivekananda Global University Online", "BBA", None, "Online BBA - Entrepreneurship", "3 Years", 75000, "10+2 in any stream", "Online"),
    ("Vivekananda Global University Online", "MCA", "Cloud Computing", "Online MCA - Cloud & DevOps", "2 Years", 98000, "Bachelor's degree with Mathematics/Computer Science", "Online"),
]

LEAD_DEFS = [
    {
        "full_name": "Ritika Sharma",
        "email": "ritika.sharma@example.com",
        "mobile": "9811100001",
        "city": "Delhi",
        "state": "Delhi",
        "interested_university": "Amity University Online",
        "interested_program": "Online MBA - Marketing",
        "message": "Wanted to know about EMI options and placement support for the MBA program.",
        "source": "Website Form",
    },
    {
        "full_name": "Aman Verma",
        "email": "aman.verma@example.com",
        "mobile": "9811100002",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "interested_university": "NMIMS Global Access",
        "interested_program": "Online M.Tech - AI & ML",
        "message": "Currently working as a software engineer, looking to upskill in AI & ML.",
        "source": "WhatsApp Enquiry",
    },
    {
        "full_name": "Sneha Reddy",
        "email": "sneha.reddy@example.com",
        "mobile": "9811100003",
        "city": "Hyderabad",
        "state": "Telangana",
        "interested_university": "Jain Online (Deemed-to-be University)",
        "interested_program": "Online MCA - Data Science",
        "message": "Need guidance on eligibility since my graduation is in Commerce, not Computer Science.",
        "source": "Google Ads",
    },
    {
        "full_name": "Karan Mehta",
        "email": "karan.mehta@example.com",
        "mobile": "9811100004",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "interested_university": "Chandigarh University Online",
        "interested_program": "Online BBA - Digital Business",
        "message": "Looking for a part-time friendly BBA program alongside my current job.",
        "source": "Referral",
    },
    {
        "full_name": "Priyanka Nair",
        "email": "priyanka.nair@example.com",
        "mobile": "9811100005",
        "city": "Kochi",
        "state": "Kerala",
        "interested_university": "Manipal University Jaipur Online",
        "interested_program": "Online MBA - HR",
        "message": "Interested in scholarship options for women applicants.",
        "source": "Instagram Ad",
    },
]

USER_DEFS = [
    {
        "full_name": "Admin User",
        "email": "admin@campusunlock.com",
        "mobile": "9900000001",
        "password": "AdminPass@123",
        "is_verified": True,
        "is_admin": True,
    },
    {
        "full_name": "Rahul Kapoor",
        "email": "rahul.kapoor@example.com",
        "mobile": "9900000002",
        "password": "UserPass@123",
        "is_verified": True,
        "is_admin": False,
    },
    {
        "full_name": "Meera Iyer",
        "email": "meera.iyer@example.com",
        "mobile": "9900000003",
        "password": "UserPass@123",
        "is_verified": False,
        "is_admin": False,
    },
]


def seed_categories():
    """Create Categories; return {name: Category} lookup."""
    categories = {}
    for name in CATEGORY_NAMES:
        slug = slugify(name)
        category, _ = get_or_create(
            Category,
            {"slug": slug},
            defaults={"name": name, "description": f"{name} programs offered across our partner universities."},
        )
        categories[name] = category
    return categories


def seed_specializations(categories):
    """Create Specializations; return {name: Specialization} lookup."""
    specializations = {}
    for name, home_category_name in SPECIALIZATION_DEFS:
        slug = slugify(name)
        specialization, _ = get_or_create(
            Specialization,
            {"slug": slug},
            defaults={
                "name": name,
                "description": f"{name} specialization.",
                "category": categories[home_category_name],
            },
        )
        specializations[name] = specialization
    return specializations


def seed_universities():
    """Create Universities; return {name: University} lookup."""
    universities = {}
    for uni in UNIVERSITY_DEFS:
        slug = slugify(uni["name"])
        university, _ = get_or_create(
            University,
            {"slug": slug},
            defaults={
                "name": uni["name"],
                "city": uni["city"],
                "state": uni["state"],
                "country": "India",
                "website": uni["website"],
                "ranking": uni["ranking"],
                "accreditation": uni["accreditation"],
                "established_year": uni["established_year"],
                "description": uni["description"],
                "is_active": True,
            },
        )
        universities[uni["name"]] = university
    return universities


def seed_programs(universities, categories, specializations):
    """Create Programs linked to their University / Category / Specialization."""
    count_created = 0
    for (
        uni_name,
        category_name,
        spec_name,
        title,
        duration,
        fees,
        eligibility,
        mode,
    ) in PROGRAM_DEFS:
        slug = slugify(f"{uni_name}-{title}")
        _, created = get_or_create(
            Program,
            {"slug": slug},
            defaults={
                "title": title,
                "duration": duration,
                "fees": fees,
                "eligibility": eligibility,
                "mode": mode,
                "description": f"{title} offered by {uni_name}, delivered fully online with recorded and live sessions.",
                "is_featured": fees >= 140000,
                "is_active": True,
                "university": universities[uni_name],
                "category": categories[category_name],
                "specialization": specializations[spec_name] if spec_name else None,
            },
        )
        if created:
            count_created += 1
    return count_created


def seed_leads():
    """Create demo Leads."""
    count_created = 0
    for lead_data in LEAD_DEFS:
        _, created = get_or_create(
            Lead,
            {"email": lead_data["email"], "full_name": lead_data["full_name"]},
            defaults={
                "mobile": lead_data["mobile"],
                "city": lead_data["city"],
                "state": lead_data["state"],
                "interested_university": lead_data["interested_university"],
                "interested_program": lead_data["interested_program"],
                "message": lead_data["message"],
                "source": lead_data["source"],
                "status": "New",
            },
        )
        if created:
            count_created += 1
    return count_created


def seed_users():
    """Create demo Users with securely hashed passwords."""
    count_created = 0
    for user_data in USER_DEFS:
        existing = User.query.filter_by(email=user_data["email"]).first()
        if existing:
            continue

        user = User(
            full_name=user_data["full_name"],
            email=user_data["email"],
            mobile=user_data["mobile"],
            is_verified=user_data["is_verified"],
            is_admin=user_data["is_admin"],
            is_active=True,
        )
        user.set_password(user_data["password"])
        db.session.add(user)
        count_created += 1
    return count_created


def run_seed():
    categories = seed_categories()
    specializations = seed_specializations(categories)
    universities = seed_universities()
    programs_created = seed_programs(universities, categories, specializations)
    leads_created = seed_leads()
    users_created = seed_users()

    return {
        "categories": len(categories),
        "specializations": len(specializations),
        "universities": len(universities),
        "programs_created": programs_created,
        "leads_created": leads_created,
        "users_created": users_created,
    }


if __name__ == "__main__":
    flask_env = os.environ.get("FLASK_ENV", "default")
    app = create_app(config_map.get(flask_env, config_map["default"]))

    with app.app_context():
        try:
            summary = run_seed()
            db.session.commit()
            print("Database Seed Completed Successfully")
            print(
                f"  Categories: {summary['categories']} | "
                f"Specializations: {summary['specializations']} | "
                f"Universities: {summary['universities']} | "
                f"Programs created: {summary['programs_created']} | "
                f"Leads created: {summary['leads_created']} | "
                f"Users created: {summary['users_created']}"
            )
        except Exception as exc:
            db.session.rollback()
            print(f"Database seed failed, rolled back: {exc}", file=sys.stderr)
            raise
