"""
Campus Unlock — Database Seed Script
======================================
Populates the database with realistic demo data:
  - 6 Categories
  - 8 Specializations
  - 108 Universities (10 original + 98 added for launch — see
    data/universities.py for the full list and data-quality notes)
  - 125+ Programs (linked to University + Category + Specialization)
  - 5 Leads
  - 3 Users (with hashed passwords via the existing User model)

Safe to run multiple times: every insert is guarded by an existence
check on a natural unique key (slug / email), so re-running this
script will not create duplicate rows. All work happens in a single
SQLAlchemy session and is committed exactly once at the end; any
failure triggers a full rollback.

University/Program *data* now lives in data/universities.py, not in
this file — seed.py only contains the seeding logic (get_or_create
calls), so the catalog can grow without this file changing.

Detail page content is sourced from TWO places, merged at runtime:
  1. data/university_details.py  — hand-curated Python entries
  2. content/university_details/ — Markdown files (one per university)

Both are parsed on every `python seed.py` run. MD files take
precedence over hand-curated entries for any field they provide, so
you can progressively migrate detail data into MD files without
touching Python. Simply drop a new .md file into the folder and run
seed.py — no other changes needed.

MD parser
---------
The parser is deterministic, offline, and pattern-based. It reads the
structured sections written by the standard detail-page MD template
(Hero, About, Highlights, Approvals, Programs, FAQs, etc.) and
converts them into the same dict shape that seed_university_details()
already expects. It never calls an API or LLM. Invalid / malformed
files are skipped with a logged warning and do not stop execution.

Usage:
    python seed.py
"""

import os
import re
import sys
import glob
import logging
from pathlib import Path
from datetime import datetime, timedelta

from app import create_app
from config import config as config_map
from models import db, Category, Specialization, University, Program, User, Lead, FAQ, Scholarship
from data.universities import UNIVERSITY_DEFS, PROGRAM_DEFS
# UNIVERSITY_DETAILS is no longer imported statically — it is loaded
# at runtime by load_md_details() + merge_details() so that any .md
# file dropped into content/university_details/ is picked up
# automatically on the next `python seed.py` run.
try:
    from data.university_details import UNIVERSITY_DETAILS as _PYTHON_DETAILS
except ImportError:
    _PYTHON_DETAILS = []

# ---------------------------------------------------------------------------
# Path to the folder containing per-university Markdown detail pages.
# Every .md file dropped here is automatically picked up on the next
# `python seed.py` run — no other changes needed.
# ---------------------------------------------------------------------------
MD_DETAILS_DIR = Path(__file__).parent / "content" / "university_details"

logger = logging.getLogger(__name__)


# ===========================================================================
# MD DETAIL PAGE PARSER
# ===========================================================================
# Reads every .md file in content/university_details/ and converts it into
# the same dict shape that seed_university_details() already consumes:
#
#   {
#     "name":              str,           # matched against University.name
#     "short_description": str | None,
#     "full_description":  str | None,
#     "why_choose":        str | None,
#     "ugc_approved":      bool | None,
#     "aicte_approved":    bool | None,
#     "aiu_member":        bool | None,
#     "wes_approved":      bool | None,
#     "placement_support": bool | None,
#     "highest_package":   float | None,
#     "average_package":   float | None,
#     "top_recruiters":    str | None,    # comma-separated
#     "meta_title":        str | None,
#     "meta_description":  str | None,
#     "faqs":              [{"question": str, "answer": str}, ...],
#     "scholarships":      [{"title": str, "description": str,
#                            "amount": float | None, "deadline": str | None}, ...],
#   }
#
# Design rules
# ------------
# • Deterministic & offline — pure regex/string ops, no LLM calls.
# • Every section is optional; missing sections produce None / [].
# • Malformed files are skipped with a warning; execution never stops.
# • Adding a new extractable section requires only one new helper here.
# • No university names or filenames are hardcoded anywhere.
# ===========================================================================

# ---------------------------------------------------------------------------
# Low-level text helpers
# ---------------------------------------------------------------------------

def _clean(text: str) -> str:
    """Strip leading/trailing whitespace and collapse inner blank lines."""
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def _extract_section(md: str, heading: str) -> str | None:
    """
    Return the text body of a Markdown ## heading block.

    Matches `## <heading>` (case-insensitive, ignoring trailing
    punctuation like '&' or ':') and returns everything up to the
    next ## heading or end-of-file.  Returns None if not found.
    """
    # Escape special regex chars in the heading, then allow optional
    # trailing punct / whitespace and ignore case.
    pattern = (
        r"^##\s+"
        + re.escape(heading).replace(r"\ ", r"\s+")
        + r"[^\n]*\n(.*?)(?=^##\s|\Z)"
    )
    m = re.search(pattern, md, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    return _clean(m.group(1))


def _strip_md_formatting(text: str) -> str:
    """
    Remove common Markdown formatting so plain text is stored in the DB:
      - bold/italic markers (* ** _ __)
      - inline code backticks
      - link syntax [text](url) → text
      - blockquote markers (>)
      - leading list markers (- * •)
      - horizontal rules (--- ***)
    """
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)   # [text](url)
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)   # bold/italic
    text = re.sub(r"_{1,2}([^_]+)_{1,2}", r"\1", text)     # underscore emphasis
    text = re.sub(r"`([^`]+)`", r"\1", text)                # inline code
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)   # blockquotes
    text = re.sub(r"^[-*•]\s+", "", text, flags=re.MULTILINE)  # list bullets
    text = re.sub(r"^[-*]{3,}\s*$", "", text, flags=re.MULTILINE)  # hr
    return _clean(text)


# ---------------------------------------------------------------------------
# Field-specific extractors
# ---------------------------------------------------------------------------

def _parse_name(md: str) -> str | None:
    """
    Extract the university name from the Hero section.
    Looks for:  - **Name:** Some University Name
    """
    m = re.search(r"-\s*\*{1,2}Name:\*{1,2}\s*(.+)", md, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Fallback: first H1 heading
    m = re.search(r"^#\s+(.+)", md, re.MULTILINE)
    if m:
        # Strip parenthetical sub-labels like "(Deemed to be University)"
        name = m.group(1).strip()
        name = re.sub(r"\s*—.*$", "", name).strip()  # drop "— Detail Page Content"
        return name
    return None


def _parse_tagline(md: str) -> str | None:
    """Extract the Tagline line from the Hero section."""
    m = re.search(
        r"-\s*\*{1,2}Tagline:\*{1,2}\s*[*_]?(.+?)[*_]?\s*$",
        md,
        re.IGNORECASE | re.MULTILINE,
    )
    if m:
        return _strip_md_formatting(m.group(1).strip())
    return None


def _parse_about(md: str) -> str | None:
    """Return the About section body as plain text."""
    body = _extract_section(md, "About")
    if body:
        return _strip_md_formatting(body)
    return None


def _parse_why_choose(md: str) -> str | None:
    """
    Return the Why Choose / Highlights section body.
    Tries 'Why Choose' first, falls back to 'Highlights'.
    """
    body = _extract_section(md, "Why Choose") or _extract_section(md, "Highlights")
    if body:
        return _strip_md_formatting(body)
    return None


def _parse_approvals(md: str) -> dict:
    """
    Parse the Approvals & Accreditations section.

    Returns a dict of booleans:
        ugc_approved, aicte_approved, aiu_member, wes_approved

    A flag is set to True only when the table row shows ✅ Yes / ✅ Approved
    (or the word 'approved'/'yes'/'confirmed' in that cell) — never from
    a ⚠️ / ❌ / None / uncertain cell.
    """
    section = _extract_section(md, "Approvals") or ""
    flags = {
        "ugc_approved": None,
        "aicte_approved": None,
        "aiu_member": None,
        "wes_approved": None,
    }

    # Mapping: keyword in the Approval column → flag name
    keyword_map = {
        "ugc": "ugc_approved",
        "aicte": "aicte_approved",
        "aiu": "aiu_member",
        "wes": "wes_approved",
    }

    # Each table row: | Approval label | ✅ Yes | ... |
    for row in re.finditer(r"\|([^|]+)\|([^|]+)\|", section):
        label_cell = row.group(1).lower()
        status_cell = row.group(2).lower()

        # Only set True on clearly positive cells
        is_confirmed = bool(
            re.search(r"✅|yes|approved|confirmed|✓", status_cell)
        ) and not re.search(r"❌|not found|no\b|unconfirmed|possibly", status_cell)

        for keyword, flag in keyword_map.items():
            if keyword in label_cell and is_confirmed:
                flags[flag] = True

    # Also scan narrative text for explicit confirmations
    # e.g. "AIU member — confirmed on the university's own official domain"
    narrative = section + "\n" + (md[:2000])  # also check early in doc
    if flags["ugc_approved"] is None and re.search(
        r"ugc[- ]deb.{0,40}(approved|confirmed|yes)", narrative, re.IGNORECASE
    ):
        flags["ugc_approved"] = True
    if flags["aicte_approved"] is None and re.search(
        r"aicte.{0,40}(approved|confirmed|yes)", narrative, re.IGNORECASE
    ):
        flags["aicte_approved"] = True
    if flags["aiu_member"] is None and re.search(
        r"aiu.{0,40}(member|confirmed|yes)", narrative, re.IGNORECASE
    ):
        flags["aiu_member"] = True
    if flags["wes_approved"] is None and re.search(
        r"wes.{0,40}(recognized|confirmed|yes)", narrative, re.IGNORECASE
    ):
        flags["wes_approved"] = True

    return flags


def _parse_placement(md: str) -> dict:
    """
    Extract placement-related fields from the Placements section.

    Returns:
        placement_support  bool | None
        highest_package    float | None   (in LPA, stored as raw float)
        average_package    float | None
        top_recruiters     str | None     (comma-separated)
    """
    section = _extract_section(md, "Placement") or ""
    result = {
        "placement_support": None,
        "highest_package": None,
        "average_package": None,
        "top_recruiters": None,
    }

    # placement_support = True if section says dedicated / true / yes
    if re.search(
        r"placement.{0,60}(true|dedicated|yes|confirmed|cell|support)",
        section,
        re.IGNORECASE,
    ):
        result["placement_support"] = True

    # highest_package: look for "₹XX LPA" or "XX lakh" near "highest"
    m = re.search(
        r"highest.{0,40}[₹]?\s*([\d.]+)\s*(?:lpa|lakh|l)",
        section,
        re.IGNORECASE,
    )
    if m:
        try:
            result["highest_package"] = float(m.group(1))
        except ValueError:
            pass

    # average_package: look for range "₹X-Y LPA" → take midpoint,
    # or a single "₹X LPA"
    m = re.search(
        r"average.{0,40}[₹]?\s*([\d.]+)\s*[-–]\s*([\d.]+)\s*(?:lpa|lakh|l)",
        section,
        re.IGNORECASE,
    )
    if m:
        try:
            lo, hi = float(m.group(1)), float(m.group(2))
            result["average_package"] = round((lo + hi) / 2, 2)
        except ValueError:
            pass
    else:
        m = re.search(
            r"average.{0,40}[₹]?\s*([\d.]+)\s*(?:lpa|lakh|l)",
            section,
            re.IGNORECASE,
        )
        if m:
            try:
                result["average_package"] = float(m.group(1))
            except ValueError:
                pass

    # top_recruiters: look for a python list or comma-separated names
    # e.g. "TCS, Wipro, Infosys" — only grab names, not generic categories
    recruiter_m = re.search(
        r"(?:recruiters?|hiring partners?)[^:\n]*:\s*([A-Z][^\n.]+)",
        section,
        re.IGNORECASE,
    )
    if recruiter_m:
        raw = recruiter_m.group(1)
        # Keep only items that look like proper company names (start with capital)
        names = [
            n.strip().strip("*_`")
            for n in re.split(r"[,;]", raw)
            if re.match(r"[A-Z]", n.strip())
        ]
        if names:
            result["top_recruiters"] = ", ".join(names)

    return result


def _parse_meta(md: str) -> dict:
    """Extract meta title and meta description from the Meta section."""
    section = _extract_section(md, "Meta") or ""
    result = {"meta_title": None, "meta_description": None}

    m = re.search(r"\*{1,2}Meta title:\*{1,2}\s*(.+)", section, re.IGNORECASE)
    if m:
        result["meta_title"] = _strip_md_formatting(m.group(1).strip())

    m = re.search(r"\*{1,2}Meta description:\*{1,2}\s*(.+)", section, re.IGNORECASE)
    if m:
        result["meta_description"] = _strip_md_formatting(m.group(1).strip())

    return result


def _parse_faqs(md: str) -> list[dict]:
    """
    Extract FAQs from the FAQs section.

    Handles two common formats:
      1. Python dict literals inside a ```python … ``` block:
             {"question": "...", "answer": "..."}
      2. Markdown Q&A pairs:
             **Q:** What is …?
             **A:** Yes …
    """
    section = _extract_section(md, "FAQ") or ""
    faqs = []

    # --- Format 1: python code block with dict literals ---
    code_m = re.search(r"```python(.*?)```", section, re.DOTALL)
    if code_m:
        block = code_m.group(1)
        # Extract each {"question": "...", "answer": "..."} dict
        pairs = re.findall(
            r'"question"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*"answer"\s*:\s*"((?:[^"\\]|\\.)*)"',
            block,
        )
        for q, a in pairs:
            q = q.replace('\\"', '"').replace("\\n", " ").strip()
            a = a.replace('\\"', '"').replace("\\n", " ").strip()
            if q and a:
                faqs.append({"question": q, "answer": a})
        if faqs:
            return faqs

    # --- Format 2: bold Q: / A: markdown pairs ---
    for m in re.finditer(
        r"\*{1,2}Q(?:uestion)?:\*{1,2}\s*(.+?)\s*\*{1,2}A(?:nswer)?:\*{1,2}\s*(.+?)(?=\*{1,2}Q|$)",
        section,
        re.DOTALL | re.IGNORECASE,
    ):
        q = _strip_md_formatting(m.group(1)).strip()
        a = _strip_md_formatting(m.group(2)).strip()
        if q and a:
            faqs.append({"question": q, "answer": a})

    return faqs


def _parse_scholarships(md: str) -> list[dict]:
    """
    Extract scholarship entries from the Scholarships section.

    Handles python dict literals inside a ```python … ``` block:
        {"title": "...", "description": "...", "amount": None, "deadline": None}
    """
    section = _extract_section(md, "Scholarship") or ""
    scholarships = []

    code_m = re.search(r"```python(.*?)```", section, re.DOTALL)
    if not code_m:
        return scholarships

    block = code_m.group(1)

    # Extract each scholarship dict; amount/deadline are optional
    for m in re.finditer(
        r'"title"\s*:\s*"((?:[^"\\]|\\.)*)"'
        r'(?:.*?"description"\s*:\s*"((?:[^"\\]|\\.)*)")?'
        r'(?:.*?"amount"\s*:\s*([^,}\n]+))?'
        r'(?:.*?"deadline"\s*:\s*([^,}\n]+))?',
        block,
        re.DOTALL,
    ):
        title = m.group(1).replace('\\"', '"').strip()
        description = (m.group(2) or "").replace('\\"', '"').strip() or None
        raw_amount = (m.group(3) or "").strip()
        raw_deadline = (m.group(4) or "").strip()

        amount = None
        if raw_amount and raw_amount.lower() not in ("none", "null", ""):
            try:
                amount = float(re.sub(r"[^\d.]", "", raw_amount))
            except ValueError:
                pass

        deadline = None
        if raw_deadline and raw_deadline.lower() not in ("none", "null", '""', ""):
            deadline = raw_deadline.strip('"\'')

        if title:
            scholarships.append(
                {
                    "title": title,
                    "description": description,
                    "amount": amount,
                    "deadline": deadline,
                }
            )

    return scholarships


# ---------------------------------------------------------------------------
# Main parser: single MD file → detail dict
# ---------------------------------------------------------------------------

def parse_md_detail(filepath: Path) -> dict | None:
    """
    Parse one university detail Markdown file into a detail dict.

    Returns None (and logs a warning) if the file cannot be parsed or
    does not contain a recognisable university name.  Never raises.
    """
    try:
        md = filepath.read_text(encoding="utf-8")
    except OSError as exc:
        logger.warning("MD parser: cannot read %s — %s", filepath.name, exc)
        return None

    # Must find a university name or we can't match it to the DB
    name = _parse_name(md)
    if not name:
        logger.warning(
            "MD parser: skipped %s — could not extract university name",
            filepath.name,
        )
        return None

    about      = _parse_about(md)
    why_choose = _parse_why_choose(md)
    approvals  = _parse_approvals(md)
    placement  = _parse_placement(md)
    meta       = _parse_meta(md)
    faqs       = _parse_faqs(md)
    scholarships = _parse_scholarships(md)

    # short_description: tagline from Hero, or first sentence of About
    short_desc = _parse_tagline(md)
    if not short_desc and about:
        first_sentence = re.split(r"(?<=[.!?])\s", about)[0]
        short_desc = first_sentence if len(first_sentence) < 300 else None

    return {
        "name":              name,
        "short_description": short_desc,
        "full_description":  about,
        "why_choose":        why_choose,
        "ugc_approved":      approvals.get("ugc_approved"),
        "aicte_approved":    approvals.get("aicte_approved"),
        "aiu_member":        approvals.get("aiu_member"),
        "wes_approved":      approvals.get("wes_approved"),
        "placement_support": placement.get("placement_support"),
        "highest_package":   placement.get("highest_package"),
        "average_package":   placement.get("average_package"),
        "top_recruiters":    placement.get("top_recruiters"),
        "meta_title":        meta.get("meta_title"),
        "meta_description":  meta.get("meta_description"),
        "faqs":              faqs,
        "scholarships":      scholarships,
        # Source tag used in summary reporting only — not written to DB
        "_source_file":      filepath.name,
    }


# ---------------------------------------------------------------------------
# Scan folder and return all parsed detail dicts
# ---------------------------------------------------------------------------

def load_md_details(directory: Path) -> tuple[list[dict], list[str], list[str]]:
    """
    Scan `directory` for *.md files, parse each one, and return:
        (parsed_details, skipped_filenames, error_filenames)

    Files that parse successfully are in parsed_details.
    Files that produce no recognisable name are in skipped_filenames.
    Files that raise an unexpected exception are in error_filenames.
    """
    parsed   = []
    skipped  = []
    errored  = []

    if not directory.exists():
        logger.info("MD details folder not found: %s — skipping MD parsing", directory)
        return parsed, skipped, errored

    md_files = sorted(directory.glob("*.md"))
    if not md_files:
        logger.info("No .md files found in %s", directory)
        return parsed, skipped, errored

    for filepath in md_files:
        try:
            result = parse_md_detail(filepath)
            if result is None:
                skipped.append(filepath.name)
            else:
                parsed.append(result)
        except Exception as exc:                      # pragma: no cover
            logger.error(
                "MD parser: unexpected error in %s — %s", filepath.name, exc,
                exc_info=True,
            )
            errored.append(filepath.name)

    return parsed, skipped, errored


# ---------------------------------------------------------------------------
# Merge MD-parsed details with hand-curated Python entries
# ---------------------------------------------------------------------------

def merge_details(python_details: list[dict], md_details: list[dict]) -> list[dict]:
    """
    Merge the two detail sources into a single list.

    Strategy: MD files take precedence over Python entries for any
    field they provide (i.e. not None / not empty list).  This lets
    you progressively migrate a Python entry into an MD file without
    having to delete the Python entry first — the MD data simply wins.

    Universities that appear only in Python entries, or only in MD
    files, are both included as-is.
    """
    # Index Python entries by name (lowercased for fuzzy match)
    by_name: dict[str, dict] = {}
    for entry in python_details:
        by_name[entry["name"].lower().strip()] = dict(entry)

    for md_entry in md_details:
        key = md_entry["name"].lower().strip()
        if key in by_name:
            # Merge: MD wins for any non-None / non-empty value
            base = by_name[key]
            for field, value in md_entry.items():
                if field == "_source_file":
                    continue
                if value is None:
                    continue
                if isinstance(value, list) and len(value) == 0:
                    continue
                base[field] = value
            by_name[key] = base
        else:
            # New university only in MD
            by_name[key] = dict(md_entry)

    return list(by_name.values())


# ===========================================================================
# END OF MD PARSER
# ===========================================================================


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

    If a row already exists, any field in `defaults` that is currently
    None/blank on that row gets backfilled from `defaults` (e.g. a
    university seeded before logo_url existed will pick it up on the
    next run). Fields that already hold a real value are left alone —
    this never overwrites data that's already been set (including
    manual edits made via the admin panel).
    """
    instance = model.query.filter_by(**lookup).first()
    if instance:
        if defaults:
            for key, value in defaults.items():
                if value is None:
                    continue
                if getattr(instance, key, None) in (None, ""):
                    setattr(instance, key, value)
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

# UNIVERSITY_DEFS and PROGRAM_DEFS now live in data/universities.py
# (imported above) so this file stays small and the data can grow
# independently of the seeding logic.

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
                "university_type": uni.get("university_type"),
                "ownership": uni.get("ownership"),
                "logo_url": uni.get("logo_url"),
                "is_active": True,
            },
        )
        universities[uni["name"]] = university
    return universities


def seed_university_details(universities, detail_list):
    """
    Backfill rich detail-page content (descriptions, approval flags,
    placement info, meta tags) onto existing University rows, and
    create their FAQs and Scholarships.

    `detail_list` is the merged result of hand-curated Python entries
    and any MD files parsed from content/university_details/ — built
    by run_seed() before this function is called.

    University-level text/numeric fields only get filled in when
    currently None/blank (same backfill semantics as get_or_create
    elsewhere in this file) — never overwrites a value someone already
    set. Boolean approval flags are only ever flipped True (never back
    to False), so confirmed research always gets written in without
    risking overwriting a manual edit.

    FAQs and Scholarships are matched by (university, question) /
    (university, title) via get_or_create(), so re-running is
    idempotent and won't duplicate rows.
    """
    bool_fields = {
        "ugc_approved", "aicte_approved", "aiu_member",
        "wes_approved", "placement_support",
    }

    faqs_created = 0
    scholarships_created = 0
    matched = 0

    for detail in detail_list:
        university = universities.get(detail["name"])
        if university is None:
            continue  # name doesn't match a seeded university — skip rather than error
        matched += 1

        fields = {
            "short_description": detail.get("short_description"),
            "full_description": detail.get("full_description"),
            "why_choose": detail.get("why_choose"),
            "ugc_approved": detail.get("ugc_approved"),
            "aicte_approved": detail.get("aicte_approved"),
            "aiu_member": detail.get("aiu_member"),
            "wes_approved": detail.get("wes_approved"),
            "placement_support": detail.get("placement_support"),
            "highest_package": detail.get("highest_package"),
            "average_package": detail.get("average_package"),
            "top_recruiters": detail.get("top_recruiters"),
            "meta_title": detail.get("meta_title"),
            "meta_description": detail.get("meta_description"),
        }
        for field, value in fields.items():
            if value is None:
                continue
            if field in bool_fields:
                if getattr(university, field, None) is not True:
                    setattr(university, field, value)
            else:
                if getattr(university, field, None) in (None, ""):
                    setattr(university, field, value)

        for faq_data in detail.get("faqs", []):
            _, created = get_or_create(
                FAQ,
                {"university": university, "question": faq_data["question"]},
                defaults={"answer": faq_data["answer"], "is_active": True},
            )
            if created:
                faqs_created += 1

        for sch_data in detail.get("scholarships", []):
            _, created = get_or_create(
                Scholarship,
                {"university": university, "title": sch_data["title"]},
                defaults={
                    "description": sch_data.get("description"),
                    "amount": sch_data.get("amount"),
                    "deadline": sch_data.get("deadline"),
                    "is_active": True,
                },
            )
            if created:
                scholarships_created += 1

    return {
        "universities_matched": matched,
        "faqs_created": faqs_created,
        "scholarships_created": scholarships_created,
    }


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
                "is_featured": bool(fees) and fees >= 140000,
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
    # ------------------------------------------------------------------
    # 1. Load and merge detail-page content from both sources:
    #    a) data/university_details.py  (hand-curated Python entries)
    #    b) content/university_details/ (Markdown files — auto-scanned)
    # ------------------------------------------------------------------
    md_parsed, md_skipped, md_errored = load_md_details(MD_DETAILS_DIR)
    merged_details = merge_details(_PYTHON_DETAILS, md_parsed)

    # ------------------------------------------------------------------
    # 2. Seed everything else
    # ------------------------------------------------------------------
    categories     = seed_categories()
    specializations = seed_specializations(categories)
    universities   = seed_universities()
    details_summary = seed_university_details(universities, merged_details)
    programs_created = seed_programs(universities, categories, specializations)
    leads_created  = seed_leads()
    users_created  = seed_users()

    return {
        "categories":                len(categories),
        "specializations":           len(specializations),
        "universities":              len(universities),
        # MD parser stats
        "md_files_parsed":           len(md_parsed),
        "md_files_skipped":          len(md_skipped),
        "md_files_errored":          len(md_errored),
        "md_skipped_names":          md_skipped,
        "md_errored_names":          md_errored,
        # Detail seeding stats
        "university_details_matched": details_summary["universities_matched"],
        "faqs_created":              details_summary["faqs_created"],
        "scholarships_created":      details_summary["scholarships_created"],
        # Rest
        "programs_created":          programs_created,
        "leads_created":             leads_created,
        "users_created":             users_created,
    }


if __name__ == "__main__":
    flask_env = os.environ.get("FLASK_ENV", "default")
    app = create_app(config_map.get(flask_env, config_map["default"]))

    with app.app_context():
        try:
            summary = run_seed()
            db.session.commit()

            print("\n" + "=" * 58)
            print("  Campus Unlock — Seed Completed Successfully")
            print("=" * 58)
            print(f"  Categories        : {summary['categories']}")
            print(f"  Specializations   : {summary['specializations']}")
            print(f"  Universities      : {summary['universities']}")
            print(f"  Programs created  : {summary['programs_created']}")
            print(f"  Leads created     : {summary['leads_created']}")
            print(f"  Users created     : {summary['users_created']}")
            print("-" * 58)
            print("  University Detail Pages")
            print(f"    MD files parsed   : {summary['md_files_parsed']}")
            print(f"    MD files skipped  : {summary['md_files_skipped']}")
            print(f"    MD files errored  : {summary['md_files_errored']}")
            print(f"    DB rows matched   : {summary['university_details_matched']}")
            print(f"    FAQs created      : {summary['faqs_created']}")
            print(f"    Scholarships      : {summary['scholarships_created']}")

            if summary["md_skipped_names"]:
                print("\n  Skipped MD files (name not found):")
                for name in summary["md_skipped_names"]:
                    print(f"    ⚠  {name}")

            if summary["md_errored_names"]:
                print("\n  Errored MD files:")
                for name in summary["md_errored_names"]:
                    print(f"    ✗  {name}")

            print("=" * 58 + "\n")

        except Exception as exc:
            db.session.rollback()
            print(f"\n✗ Database seed failed, rolled back: {exc}", file=sys.stderr)
            raise
