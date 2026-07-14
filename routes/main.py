"""
Campus Unlock — Main Blueprint
==========================
Houses the home route, universal /search API, and the new database-
powered /filter API. Placeholder routes return HTTP 501 for pages not
yet built so nav links never hit a raw 404/500 during development.

The home route ("/") loads Universities/Programs/Categories/
Specializations from SQLite via SQLAlchemy and passes them to
index.html as both template objects (server-rendered showcase sections)
and a JSON payload (consumed by app.js for comparison, wizard, EMI
calculator, and recently-viewed — everything that still runs client-
side and does NOT need server filtering).

/filter is the new database-powered endpoint.  It accepts every filter
the existing filter sidebar exposes, runs a single eager-loaded query,
and returns a JSON array of university dicts that match the exact shape
app.js already uses for appData.universities — so the existing
renderResults() card template works without modification.
"""

import re
from datetime import datetime
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    render_template_string,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    flash,
)

from sqlalchemy import or_, and_, func
from sqlalchemy.orm import joinedload

from models import (
    University,
    Program,
    Category,
    Specialization,
    Scholarship,
    FAQ,
    PlacementPartner,
    db,
)
from models.lead import Lead
from models.user import User
from models.saved import SavedUniversity, SavedProgram
from models.history import RecentlyViewed, CompareHistory, BrochureDownload

main_bp = Blueprint("main", __name__)

# ---------------------------------------------------------------------------
# Auth constants/helpers (merged from the former routes/auth.py)
# ---------------------------------------------------------------------------
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MIN_PASSWORD_LENGTH = 8


def _digits_only(value):
    """Strip everything but digits from a raw mobile number string."""
    return re.sub(r"\D", "", value or "")


def login_required(view):
    """Redirect anonymous visitors to /login, preserving the original
    destination via ?next=, instead of letting the view execute."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "error")
            return redirect(url_for("main.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    """
    Phase 8A — Admin System foundation.

    Gate a view behind two checks, in order:
      1. Logged in (same redirect-to-login behavior as login_required)
      2. session user's role == "admin"

    Non-admins (including logged-out visitors) never reach the view.
    A logged-in non-admin is redirected to their own dashboard rather
    than shown a raw 403, so student functionality is never disrupted.
    """

    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to continue.", "error")
            return redirect(url_for("main.login", next=request.path))

        user = User.query.get(user_id)
        if user is None or not user.is_active:
            session.pop("user_id", None)
            flash("Please log in to continue.", "error")
            return redirect(url_for("main.login", next=request.path))

        if not user.is_admin_role():
            flash("You do not have permission to access that page.", "error")
            return redirect(url_for("main.dashboard"))

        return view(*args, **kwargs)

    return wrapped

_COMING_SOON_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ page_name }} — Coming Soon | Campus Unlock</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Inter, system-ui, sans-serif; text-align: center; padding: 80px 20px; color:#1e293b;">
  <h1 style="font-size: 28px; margin-bottom: 12px;">🚧 {{ page_name }} is coming soon</h1>
  <p style="color:#64748b; margin-bottom: 24px;">We're still building this page. Please check back shortly.</p>
  <a href="/" style="color:#2563eb; text-decoration:none; font-weight:600;">&larr; Back to Home</a>
</body>
</html>
"""

# Category name -> degree level used by the "#fDegree" (Bachelor/Master) filter.
_CATEGORY_DEGREE_LEVEL = {
    "MBA": "Master",
    "MCA": "Master",
    "M.Tech": "Master",
    "BCA": "Bachelor",
    "BBA": "Bachelor",
    "B.Tech": "Bachelor",
}

# Category name -> representative emoji for program showcase cards.
_CATEGORY_EMOJI = {
    "MBA": "🎓",
    "MCA": "💻",
    "BCA": "🖥️",
    "BBA": "📊",
    "B.Tech": "⚙️",
    "M.Tech": "🔬",
}


def _coming_soon(page_name):
    """Render a minimal inline 'Coming Soon' page with a 501 status."""
    return render_template_string(_COMING_SOON_TEMPLATE, page_name=page_name), 501


def _avatar_initials(name):
    """Deterministic 2-letter avatar from a university's real name."""
    skip = {"of", "the", "and", "for", "online"}
    words = [w for w in name.replace("(", " ").replace(")", " ").split() if w.lower() not in skip]
    letters = "".join(w[0] for w in words[:2] if w)
    return (letters or name[:2]).upper()


def _serialize_program(program):
    """
    Build the plain-dict view used both for the server-rendered program
    cards and for the JSON payload app.js reads.
    """
    category_name = program.category.name if program.category else None
    specialization_name = program.specialization.name if program.specialization else None
    university_name = program.university.name if program.university else None

    return {
        "id": str(program.id),
        "name": program.title,
        "title": program.title,
        "category": category_name,
        "specialization": specialization_name,
        "university": university_name,
        "fees": float(program.fees) if program.fees is not None else None,
        "duration": program.duration,
        "eligibility": program.eligibility,
        "mode": program.mode,
        "is_featured": bool(program.is_featured),
        "emoji": _CATEGORY_EMOJI.get(category_name, "🎓"),
    }


def _serialize_university(university, active_programs):
    """
    Build the plain-dict view used for university cards (both server-
    rendered and the /filter JSON response).  Shape is kept identical to
    the original so app.js card templates need no changes.
    """
    fees = [float(p.fees) for p in active_programs if p.fees is not None]
    min_fee = min(fees) if fees else None

    duration = None
    if active_programs:
        if min_fee is not None:
            match = next(
                (p for p in active_programs if p.fees is not None and float(p.fees) == min_fee),
                active_programs[0],
            )
            duration = match.duration
        else:
            duration = active_programs[0].duration

    modes = [p.mode for p in active_programs if p.mode]
    mode = max(set(modes), key=modes.count) if modes else "Online"

    specs = sorted({p.specialization.name for p in active_programs if p.specialization})
    degrees = sorted(
        {_CATEGORY_DEGREE_LEVEL.get(p.category.name, "Master") for p in active_programs if p.category}
    ) or ["Bachelor", "Master"]

    return {
        "id": str(university.id),
        "slug": university.slug,
        "name": university.name,
        "logo": university.logo,
        "naac": university.accreditation,
        "nirf": university.ranking,
        "rating": None,
        "placement": None,
        "emi": None,
        "fee": min_fee,
        "duration": duration,
        "state": university.state,
        "city": university.city,
        "mode": mode,
        "programs": [p.title for p in active_programs],
        "specs": specs,
        "degree": degrees,
        "avatar": _avatar_initials(university.name),
    }


def _load_campus_data():
    """
    Single efficient query: fetch active universities with their active
    programs (and each program's category/specialization) eager-loaded.
    """
    universities = (
        University.query.filter_by(is_active=True)
        .options(
            joinedload(University.programs).joinedload(Program.category),
            joinedload(University.programs).joinedload(Program.specialization),
        )
        .all()
    )

    university_programs = {
        uni.id: [p for p in uni.programs if p.is_active] for uni in universities
    }

    serialized_universities = [
        _serialize_university(uni, university_programs[uni.id]) for uni in universities
    ]
    serialized_programs = [
        _serialize_program(p)
        for uni in universities
        for p in university_programs[uni.id]
    ]

    top_universities = sorted(
        serialized_universities,
        key=lambda u: (u["nirf"] is None, u["nirf"] if u["nirf"] is not None else 0),
    )[:6]

    featured_programs = [p for p in serialized_programs if p["is_featured"]]
    if not featured_programs:
        featured_programs = serialized_programs[:9]

    return {
        "top_universities": top_universities,
        "featured_programs": featured_programs,
        "campus_data": {
            "universities": serialized_universities,
            "programs": serialized_programs,
        },
    }


def _compute_stats():
    """
    Compute site-wide statistics for display in the results section header.

    Returns a dict with:
      total_universities  — count of active universities
      total_programs      — count of active programs
      total_states        — count of distinct states with active universities
      total_specializations — count of distinct active specializations

    All queries are single-column COUNT / COUNT DISTINCT — sub-millisecond
    on SQLite even with thousands of rows.
    """
    try:
        total_universities = University.query.filter_by(is_active=True).count()
        total_programs = Program.query.filter_by(is_active=True).count()
        total_states = (
            University.query
            .filter(University.is_active.is_(True), University.state.isnot(None))
            .with_entities(func.count(func.distinct(University.state)))
            .scalar() or 0
        )
        total_specializations = (
            Specialization.query.count()
        )
    except Exception:
        total_universities = 0
        total_programs = 0
        total_states = 0
        total_specializations = 0

    return {
        "total_universities": total_universities,
        "total_programs": total_programs,
        "total_states": total_states,
        "total_specializations": total_specializations,
    }


# ---------------------------------------------------------------------------
# Fallback scholarship cards shown when the DB has no active global entries.
# ---------------------------------------------------------------------------
_FALLBACK_SCHOLARSHIPS = [
    {
        "amount_label": "Up to 20%",
        "title": "Merit Scholarship",
        "description": "For students with strong academic records in their previous qualifying degree.",
        "is_fallback": True,
    },
    {
        "amount_label": "Up to 15%",
        "title": "Women in Tech Grant",
        "description": "Supporting women enrolling in MCA, BCA, and M.Tech programs.",
        "is_fallback": True,
    },
    {
        "amount_label": "No-cost EMI",
        "title": "Easy Payment Plans",
        "description": "Split your fees into monthly instalments with 0% processing charges.",
        "is_fallback": True,
    },
]


def _format_amount_label(scholarship):
    """
    Derive a short display label for a scholarship's value.

    Priority:
      1. If the model exposes a ``discount_pct`` field, use "Up to X%".
      2. If ``amount`` is < 1 (i.e. a fraction like 0.20), treat as a
         percentage: "Up to 20%".
      3. If ``amount`` >= 1, treat as an absolute INR value: "₹X,XXX".
      4. Fall back to the scholarship title.
    """
    try:
        # Try percentage-style field first (future-proof)
        pct = getattr(scholarship, "discount_pct", None)
        if pct is not None:
            return f"Up to {int(pct)}%"

        amt = scholarship.amount
        if amt is None:
            return scholarship.title or "Scholarship"

        amt = float(amt)
        if 0 < amt <= 1:
            # Stored as decimal fraction, e.g. 0.20 → "Up to 20%"
            return f"Up to {int(amt * 100)}%"
        if amt < 100:
            # Stored as integer percentage, e.g. 20 → "Up to 20%"
            return f"Up to {int(amt)}%"
        # Stored as rupee amount
        return f"₹{int(amt):,}"
    except Exception:
        return scholarship.title or "Scholarship"


def _load_global_scholarships(limit=3):
    """
    Load the top ``limit`` active scholarships that are NOT tied to a
    specific university (university_id IS NULL), ordered by sort_order
    then id.  Falls back to the three hardcoded cards when no rows exist.
    """
    try:
        rows = (
            Scholarship.query
            .filter(Scholarship.is_active.is_(True))
            .filter(
                or_(
                    ~Scholarship.__table__.columns.keys().__contains__("university_id"),
                    Scholarship.university_id.is_(None),
                )
            )
            .order_by(
                # sort_order may not exist on all schema versions — safe fallback
                Scholarship.id
            )
            .limit(limit)
            .all()
        )
    except Exception:
        # university_id column might not exist in this schema version;
        # fall back to fetching any active scholarships.
        try:
            rows = (
                Scholarship.query
                .filter(Scholarship.is_active.is_(True))
                .order_by(Scholarship.id)
                .limit(limit)
                .all()
            )
        except Exception:
            rows = []

    if not rows:
        return _FALLBACK_SCHOLARSHIPS

    return [
        {
            "amount_label": _format_amount_label(s),
            "title": s.title,
            "description": s.description or "",
            "deadline": s.deadline,
            "is_fallback": False,
        }
        for s in rows
    ]


def _serialize_search_result(program):
    """
    Build the flat JSON shape for a single /search result.
    """
    university = program.university
    category = program.category
    specialization = program.specialization

    return {
        "university": university.name if university else None,
        "program": program.title,
        "category": category.name if category else None,
        "specialization": specialization.name if specialization else None,
        "city": university.city if university else None,
        "duration": program.duration,
        "fees": float(program.fees) if program.fees is not None else None,
        "mode": program.mode,
        "slug": program.slug,
    }


# ---------------------------------------------------------------------------
# /filter — Database-powered multi-filter endpoint
# ---------------------------------------------------------------------------

def _parse_filter_params(args):
    """
    Parse and sanitise all query-string filter params from the request.
    Returns a plain dict; missing / empty values become None / 0 so the
    calling code can use simple truthiness checks.

    Supported params
    ----------------
    search   str   — free-text across name / city / state / program titles
    degree   str   — "Bachelor" | "Master"
    program  str   — exact program title match (e.g. "Online MBA")
    category str   — exact Category.name match (e.g. "MBA")
    spec     str   — partial Specialization.name match
    budget   int   — maximum fees per year (inclusive)
    naac     str   — exact NAAC grade string (e.g. "A+")
    nirf     int   — maximum NIRF rank (inclusive)
    duration str   — exact duration string (e.g. "2 Years")
    state    str   — exact state name
    city     str   — exact city name
    mode     str   — exact mode string (e.g. "Online")
    sort     str   — "fee-asc" | "fee-desc" | "nirf-asc" | "rating-desc"
    page     int   — 1-based page number
    page_size int  — results per page (max 20)
    """
    def _str(key):
        v = (args.get(key) or "").strip()
        return v if v else None

    def _int(key, default=0):
        try:
            return int(args.get(key) or 0)
        except (ValueError, TypeError):
            return default

    return {
        "search":    _str("search"),
        "degree":    _str("degree"),
        "program":   _str("program"),
        "category":  _str("category"),
        "spec":      _str("spec"),
        "budget":    _int("budget"),
        "naac":      _str("naac"),
        "nirf":      _int("nirf"),
        "duration":  _str("duration"),
        "state":     _str("state"),
        "city":      _str("city"),
        "mode":      _str("mode"),
        "sort":      _str("sort") or "nirf-asc",
        "page":      max(1, _int("page", 1)),
        "page_size": min(20, max(1, _int("page_size", 4))),
    }


def _build_filter_query(f):
    """
    Build a SQLAlchemy query that applies all active filter dimensions
    at the database level so Python never has to scan the full table.

    Strategy
    --------
    • Join Program → Category and Program → Specialization once.
    • Apply each filter as a WHERE clause only when the user supplied a
      non-empty value — combining all active conditions with AND.
    • Eager-load relationships so _serialize_university() incurs zero
      additional queries (prevents N+1).
    • DISTINCT on University.id so a university with many matching
      programs doesn't appear multiple times.
    """
    # Start from University; we'll join through Program to reach
    # Category / Specialization for the filter conditions.
    query = (
        University.query
        .filter(University.is_active.is_(True))
        .join(University.programs)
        .filter(Program.is_active.is_(True))
        .outerjoin(Program.category)
        .outerjoin(Program.specialization)
        .options(
            joinedload(University.programs).joinedload(Program.category),
            joinedload(University.programs).joinedload(Program.specialization),
        )
        .distinct()
    )

    # --- Free-text search -------------------------------------------------
    if f["search"]:
        like = f"%{f['search']}%"
        query = query.filter(
            or_(
                University.name.ilike(like),
                University.city.ilike(like),
                University.state.ilike(like),
                Program.title.ilike(like),
                Category.name.ilike(like),
                Specialization.name.ilike(like),
            )
        )

    # --- Category (e.g. "MBA", "MCA") ------------------------------------
    if f["category"]:
        query = query.filter(Category.name == f["category"])

    # --- Degree level ("Bachelor" / "Master") ----------------------------
    # Derive the expected Category names for the requested degree level.
    if f["degree"]:
        degree_categories = [
            cat for cat, lvl in _CATEGORY_DEGREE_LEVEL.items()
            if lvl == f["degree"]
        ]
        if degree_categories:
            query = query.filter(Category.name.in_(degree_categories))

    # --- Exact program title match ----------------------------------------
    if f["program"]:
        query = query.filter(Program.title == f["program"])

    # --- Specialization (partial match) ----------------------------------
    if f["spec"]:
        query = query.filter(Specialization.name.ilike(f"%{f['spec']}%"))

    # --- Fee / budget cap -------------------------------------------------
    # A university qualifies if AT LEAST ONE of its programs is within budget.
    if f["budget"]:
        query = query.filter(
            and_(Program.fees.isnot(None), Program.fees <= f["budget"])
        )

    # --- NAAC grade -------------------------------------------------------
    if f["naac"]:
        query = query.filter(University.accreditation == f["naac"])

    # --- NIRF rank (lower is better) -------------------------------------
    if f["nirf"]:
        query = query.filter(
            and_(University.ranking.isnot(None), University.ranking <= f["nirf"])
        )

    # --- Duration ---------------------------------------------------------
    if f["duration"]:
        query = query.filter(Program.duration == f["duration"])

    # --- State / City -----------------------------------------------------
    if f["state"]:
        query = query.filter(University.state == f["state"])

    if f["city"]:
        query = query.filter(University.city == f["city"])

    # --- Mode -------------------------------------------------------------
    if f["mode"]:
        query = query.filter(Program.mode == f["mode"])

    return query


def _sort_universities(universities, sort_key):
    """
    Sort a list of serialised university dicts in Python after the DB
    query has already narrowed the result set.  Keeps None-valued fields
    at the end gracefully.
    """
    def _safe(val, default):
        return val if val is not None else default

    if sort_key == "fee-asc":
        return sorted(universities, key=lambda u: _safe(u["fee"], float("inf")))
    if sort_key == "fee-desc":
        return sorted(universities, key=lambda u: _safe(u["fee"], 0), reverse=True)
    if sort_key == "nirf-asc":
        return sorted(universities, key=lambda u: _safe(u["nirf"], float("inf")))
    if sort_key == "rating-desc":
        return sorted(universities, key=lambda u: _safe(u["rating"], 0), reverse=True)
    # Default: NIRF ascending (best rank first)
    return sorted(universities, key=lambda u: _safe(u["nirf"], float("inf")))


@main_bp.route("/filter")
def filter_universities():
    """
    Database-powered multi-filter API.

    GET /filter?search=MBA&category=MBA&state=Delhi&budget=200000&...

    All params are optional.  Missing / empty params are ignored so the
    caller can always fire the same request shape regardless of which
    filters the user has actually set.

    Response shape
    --------------
    {
      "total": <int>,          // total matching universities (pre-pagination)
      "page": <int>,
      "page_size": <int>,
      "total_pages": <int>,
      "universities": [ <university dict>, … ]
    }

    Each university dict is the same shape _serialize_university()
    produces, so app.js renderResults() works unchanged.

    Performance
    -----------
    • Single DISTINCT JOIN query with eager-loaded relationships.
    • No N+1 queries: program/category/spec data is loaded in the same
      round-trip via joinedload.
    • Pagination is done in Python after serialisation (result sets for
      an educational directory are small; full table scans hit SQLite
      sub-millisecond even with thousands of rows).
    """
    f = _parse_filter_params(request.args)

    try:
        query = _build_filter_query(f)
        universities = query.all()
    except Exception:
        # Degrade gracefully — return empty result set rather than 500.
        return jsonify({
            "total": 0,
            "page": 1,
            "page_size": f["page_size"],
            "total_pages": 1,
            "universities": [],
        })

    # Serialise: keep only active programs for each university so fee /
    # duration / specs are computed from the correct subset.
    serialized = []
    for uni in universities:
        active_programs = [p for p in uni.programs if p.is_active]

        # If a category / degree / spec / duration / mode / budget filter
        # is active, restrict the programs used for card display to only
        # the matching subset so displayed info is consistent with the
        # filter (e.g. showing MBA fee when MBA is selected, not MCA fee).
        display_programs = active_programs

        if f["category"]:
            filtered = [p for p in active_programs if p.category and p.category.name == f["category"]]
            if filtered:
                display_programs = filtered

        if f["degree"]:
            degree_cats = [c for c, lvl in _CATEGORY_DEGREE_LEVEL.items() if lvl == f["degree"]]
            filtered = [p for p in display_programs if p.category and p.category.name in degree_cats]
            if filtered:
                display_programs = filtered

        if f["program"]:
            filtered = [p for p in display_programs if p.title == f["program"]]
            if filtered:
                display_programs = filtered

        if f["spec"]:
            filtered = [p for p in display_programs if p.specialization and f["spec"].lower() in p.specialization.name.lower()]
            if filtered:
                display_programs = filtered

        if f["duration"]:
            filtered = [p for p in display_programs if p.duration == f["duration"]]
            if filtered:
                display_programs = filtered

        if f["mode"]:
            filtered = [p for p in display_programs if p.mode == f["mode"]]
            if filtered:
                display_programs = filtered

        if f["budget"]:
            filtered = [p for p in display_programs if p.fees is not None and float(p.fees) <= f["budget"]]
            if filtered:
                display_programs = filtered

        serialized.append(_serialize_university(uni, display_programs))

    # Sort in Python
    serialized = _sort_universities(serialized, f["sort"])

    # Paginate
    total = len(serialized)
    page_size = f["page_size"]
    total_pages = max(1, -(-total // page_size))  # ceiling division
    page = min(f["page"], total_pages)
    start = (page - 1) * page_size
    page_data = serialized[start: start + page_size]

    return jsonify({
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "universities": page_data,
    })


@main_bp.route("/search")
def search():
    """
    Universal search API.

    GET /search?q=<term>

    Case-insensitive partial match across University name/city/state,
    Program title, Category name, and Specialization name. Returns a
    JSON array (max 10 results, deduplicated by program). Never raises:
    a query under 2 characters, no matches, or any unexpected error all
    resolve to an empty array.
    """
    query_text = (request.args.get("q") or "").strip()

    if len(query_text) < 2:
        return jsonify([])

    try:
        like_pattern = f"%{query_text}%"

        matches = (
            Program.query.join(Program.university)
            .outerjoin(Program.category)
            .outerjoin(Program.specialization)
            .options(
                joinedload(Program.university),
                joinedload(Program.category),
                joinedload(Program.specialization),
            )
            .filter(Program.is_active.is_(True))
            .filter(
                or_(
                    Program.title.ilike(like_pattern),
                    University.name.ilike(like_pattern),
                    University.city.ilike(like_pattern),
                    University.state.ilike(like_pattern),
                    Category.name.ilike(like_pattern),
                    Specialization.name.ilike(like_pattern),
                )
            )
            .distinct()
            .limit(10)
            .all()
        )
    except Exception:
        return jsonify([])

    seen_program_ids = set()
    results = []
    for program in matches:
        if program.id in seen_program_ids:
            continue
        seen_program_ids.add(program.id)
        results.append(_serialize_search_result(program))

    return jsonify(results)


@main_bp.route("/")
def index():
    """
    Home page — backed by SQLAlchemy data.

    Passes to index.html:
      top_universities    — list of up to 6 serialised university dicts (NIRF sorted)
      featured_programs   — list of up to 9 featured / fallback program dicts
      campus_data         — full universities + programs JSON for app.js
      scholarships        — list of up to 3 global scholarship dicts for the
                            scholarships section (falls back to hardcoded cards)
      stats               — dict of site-wide counts for the results section header
    """
    data = _load_campus_data()
    scholarships = _load_global_scholarships(limit=3)
    stats = _compute_stats()

    return render_template(
        "index.html",
        top_universities=data["top_universities"],
        featured_programs=data["featured_programs"],
        campus_data=data["campus_data"],
        scholarships=scholarships,
        stats=stats,
    )


@main_bp.route("/lead", methods=["POST"])
def submit_lead():
    """
    AJAX lead capture endpoint.

    Accepts JSON: { name, phone, email, program, university }

    Validation
    ----------
    • name    — required, ≥ 2 characters
    • email   — required, basic format check
    • phone   — required, exactly 10 digits after stripping non-digits
    • program — required, non-empty

    Duplicate check
    ---------------
    A lead is a duplicate when the same email + university + program
    combination already exists in the leads table.  Returns 409 with an
    explanatory error message so the frontend can surface it inline.

    Success
    -------
    201 { "ok": true, "id": <lead_id> }

    Validation failure
    ------------------
    400 { "error": "<first failing field message>" }

    Duplicate
    ---------
    409 { "error": "You've already registered interest in this program …" }
    """
    import re

    data = request.get_json(silent=True) or {}

    # ---- Field extraction ------------------------------------------------
    name      = (data.get("name") or "").strip()
    email     = (data.get("email") or "").strip().lower()
    phone_raw = (data.get("phone") or "")
    phone     = re.sub(r"\D", "", str(phone_raw))
    program   = (data.get("program") or "").strip()
    university = (data.get("university") or "").strip()

    # ---- Server-side validation ------------------------------------------
    if len(name) < 2:
        return jsonify({"error": "Please enter your full name (at least 2 characters)."}), 400

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return jsonify({"error": "Please enter a valid email address."}), 400

    if len(phone) != 10:
        return jsonify({"error": "Please enter a valid 10-digit mobile number."}), 400

    if not program:
        return jsonify({"error": "Please select the program you are interested in."}), 400

    # ---- Duplicate check -------------------------------------------------
    try:
        duplicate = Lead.query.filter_by(
            email=email,
            interested_university=university or None,
            interested_program=program,
        ).first()
    except Exception:
        duplicate = None

    if duplicate:
        prog_label = program or "this program"
        uni_label  = f" at {university}" if university else ""
        return jsonify({
            "error": (
                f"You've already registered interest in {prog_label}{uni_label}. "
                "A counsellor will be in touch soon."
            )
        }), 409

    # ---- Persist ---------------------------------------------------------
    try:
        lead = Lead(
            full_name=name,
            email=email,
            mobile=phone,
            interested_university=university or None,
            interested_program=program,
            source="modal",
            status="New",
        )
        db.session.add(lead)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        return jsonify({"error": "Could not save your enquiry. Please try again shortly."}), 500

    return jsonify({"ok": True, "id": lead.id}), 201


@main_bp.route("/about")
def about():
    return _coming_soon("About Us")


@main_bp.route("/contact")
def contact():
    return _coming_soon("Contact")


@main_bp.route("/programs")
def programs():
    return _coming_soon("Programs")


@main_bp.route("/universities")
def universities():
    return _coming_soon("Universities")


@main_bp.route("/blog")
def blog():
    return _coming_soon("Blog")


@main_bp.route("/compare")
def compare():
    """
    Compare API — GET /compare?ids=<comma-separated university IDs>

    Phase 7C-2: when a logged-in user sends at least 2 IDs, a CompareHistory
    row is written so the dashboard can show "Recent Comparisons".

    The endpoint is intentionally separate from the coming-soon Compare page
    so the existing app.js renderCompareTable() call path is not broken.
    """
    ids_param = request.args.get("ids", "").strip()

    # No IDs supplied — this is the Compare page navigation, not the API.
    # Keep the page as coming-soon so existing nav still works.
    if not ids_param:
        return _coming_soon("Compare")

    # Parse and validate IDs
    raw_ids = [x.strip() for x in ids_param.split(",") if x.strip()]
    try:
        int_ids = [int(i) for i in raw_ids]
    except ValueError:
        return jsonify({"error": "Invalid university IDs."}), 400

    if len(int_ids) < 2:
        return jsonify({"error": "Please select at least two universities."}), 400

    if len(int_ids) > 4:
        return jsonify({"error": "You can compare a maximum of four universities."}), 400

    universities = (
        University.query
        .filter(University.id.in_(int_ids), University.is_active.is_(True))
        .options(
            joinedload(University.programs).joinedload(Program.category),
            joinedload(University.programs).joinedload(Program.specialization),
        )
        .all()
    )

    if not universities:
        return jsonify({"error": "No matching universities found."}), 404

    # Phase 7C-2: persist compare history for logged-in users
    if session.get("user_id") and len(universities) >= 2:
        try:
            names_str = ", ".join(u.name for u in universities)
            ids_str   = ", ".join(str(u.id) for u in universities)
            ch = CompareHistory(
                user_id=session["user_id"],
                university_ids=ids_str,
                university_names=names_str,
            )
            db.session.add(ch)
            db.session.commit()
        except Exception:
            db.session.rollback()

    result = []
    for u in universities:
        active_programs = [p for p in u.programs if p.is_active]
        min_fee = min(
            (float(p.fees) for p in active_programs if p.fees is not None),
            default=None,
        )
        categories    = sorted({p.category.name for p in active_programs if p.category})
        specializations = sorted({p.specialization.name for p in active_programs if p.specialization})
        modes         = sorted({p.mode for p in active_programs if p.mode})

        result.append({
            "id":               str(u.id),
            "name":             u.name,
            "slug":             u.slug,
            "logo":             u.logo_url or u.logo,
            "avatar":           _avatar_initials(u.name),
            "naac":             u.accreditation,
            "nirf":             u.ranking,
            "established_year": u.established_year,
            "city":             u.city,
            "state":            u.state,
            "website":          u.website,
            "min_fee":          min_fee,
            "categories":       categories,
            "specializations":  specializations,
            "modes":            modes,
            "programs": [
                {"title": p.title, "duration": p.duration}
                for p in active_programs[:5]
            ],
        })

    return jsonify({"universities": result})


@main_bp.route("/scholarships")
def scholarships():
    return _coming_soon("Scholarships")


def _record_recently_viewed(user_id, university_id, program_id):
    """
    Upsert a recently-viewed row for (user, university|program).

    Strategy: delete the existing row for the same (user, item) if it
    exists, then insert a fresh one with the current timestamp.  This
    keeps the list chronologically sorted by viewed_at DESC without
    needing a partial-index UPSERT that SQLite can't do cleanly.

    Enforces a per-user limit of 10 rows per item type (university /
    program) — the oldest rows beyond the limit are pruned in the same
    transaction.
    """
    LIMIT = 10

    if university_id:
        # Remove stale row for this exact university
        RecentlyViewed.query.filter_by(
            user_id=user_id, university_id=university_id
        ).delete()
        db.session.add(RecentlyViewed(user_id=user_id, university_id=university_id))
        db.session.flush()

        # Prune to LIMIT: keep newest LIMIT rows, delete the rest
        old_ids = (
            db.session.query(RecentlyViewed.id)
            .filter(
                RecentlyViewed.user_id == user_id,
                RecentlyViewed.university_id.isnot(None),
            )
            .order_by(RecentlyViewed.viewed_at.desc())
            .offset(LIMIT)
            .all()
        )
        if old_ids:
            RecentlyViewed.query.filter(
                RecentlyViewed.id.in_([r.id for r in old_ids])
            ).delete(synchronize_session=False)

    elif program_id:
        RecentlyViewed.query.filter_by(
            user_id=user_id, program_id=program_id
        ).delete()
        db.session.add(RecentlyViewed(user_id=user_id, program_id=program_id))
        db.session.flush()

        old_ids = (
            db.session.query(RecentlyViewed.id)
            .filter(
                RecentlyViewed.user_id == user_id,
                RecentlyViewed.program_id.isnot(None),
            )
            .order_by(RecentlyViewed.viewed_at.desc())
            .offset(LIMIT)
            .all()
        )
        if old_ids:
            RecentlyViewed.query.filter(
                RecentlyViewed.id.in_([r.id for r in old_ids])
            ).delete(synchronize_session=False)

    db.session.commit()


# ---------------------------------------------------------------------------
# /university/<slug> — Database-driven University Details Page
# ---------------------------------------------------------------------------

def _serialize_scholarship(scholarship):
    """Plain-dict view of a Scholarship for the details-page template."""
    return {
        "title": scholarship.title,
        "description": scholarship.description,
        "amount": float(scholarship.amount) if scholarship.amount is not None else None,
        "deadline": scholarship.deadline,
    }


def _serialize_faq(faq):
    """Plain-dict view of an FAQ for the details-page template."""
    return {"question": faq.question, "answer": faq.answer}


def _serialize_placement_partner(partner):
    """Plain-dict view of a PlacementPartner for the details-page template."""
    return {"name": partner.company_name, "logo": partner.logo_url}


def _get_similar_universities(university, limit=4):
    """
    Recommendation rail for the details page: same state first, then
    universities sharing at least one Program category, excluding the
    current university. Only active universities/programs are considered.
    Returns plain dicts in the same shape as the homepage university cards
    (via the shared _serialize_university helper), so the same uni-card
    markup/CSS can be reused without changes.
    """
    same_state = []
    if university.state:
        same_state = (
            University.query.filter(
                University.is_active.is_(True),
                University.id != university.id,
                University.state == university.state,
            )
            .options(
                joinedload(University.programs).joinedload(Program.category),
                joinedload(University.programs).joinedload(Program.specialization),
            )
            .limit(limit)
            .all()
        )

    remaining = limit - len(same_state)
    same_category = []
    if remaining > 0:
        category_ids = {
            p.category_id
            for p in university.programs
            if p.is_active and p.category_id
        }
        if category_ids:
            exclude_ids = {university.id} | {u.id for u in same_state}
            same_category = (
                University.query.join(University.programs)
                .filter(
                    University.is_active.is_(True),
                    Program.is_active.is_(True),
                    Program.category_id.in_(category_ids),
                    ~University.id.in_(exclude_ids),
                )
                .options(
                    joinedload(University.programs).joinedload(Program.category),
                    joinedload(University.programs).joinedload(Program.specialization),
                )
                .distinct()
                .limit(remaining)
                .all()
            )

    combined = same_state + same_category
    return [
        _serialize_university(uni, [p for p in uni.programs if p.is_active])
        for uni in combined
    ]


@main_bp.route("/university/<slug>")
def university_detail(slug):
    """
    Fully database-driven University Details Page.

    Loads a single active university plus every related collection
    (active programs w/ category + specialization, scholarships, FAQs,
    placement partners) in one round-trip via joinedload — no N+1
    queries — and a small "similar universities" recommendation set.
    404s automatically for an unknown or inactive slug.
    """
    university = (
        University.query.filter_by(slug=slug, is_active=True)
        .options(
            joinedload(University.programs).joinedload(Program.category),
            joinedload(University.programs).joinedload(Program.specialization),
            joinedload(University.scholarships),
            joinedload(University.faqs),
            joinedload(University.placement_partners),
        )
        .first_or_404()
    )

    active_programs = [p for p in university.programs if p.is_active]
    programs = [_serialize_program(p) for p in active_programs]

    active_scholarships = [s for s in university.scholarships if s.is_active]
    scholarships_list = [_serialize_scholarship(s) for s in active_scholarships]

    active_faqs = sorted(
        (f for f in university.faqs if f.is_active),
        key=lambda f: (f.sort_order is None, f.sort_order, f.id),
    )
    faqs = [_serialize_faq(f) for f in active_faqs]

    active_partners = [p for p in university.placement_partners if p.is_active]
    placement_partners = [_serialize_placement_partner(p) for p in active_partners]

    top_recruiters = []
    if university.top_recruiters:
        top_recruiters = [r.strip() for r in university.top_recruiters.split(",") if r.strip()]

    similar_universities = _get_similar_universities(university)

    # Phase 7C-1: has the current user saved this university?
    is_saved = False
    if session.get("user_id"):
        is_saved = SavedUniversity.query.filter_by(
            user_id=session["user_id"],
            university_id=university.id,
        ).first() is not None

    # Phase 7C-2: record recently-viewed (collapse duplicate, keep newest)
    if session.get("user_id"):
        try:
            _record_recently_viewed(
                user_id=session["user_id"],
                university_id=university.id,
                program_id=None,
            )
        except Exception:
            db.session.rollback()

    return render_template(
        "university_details.html",
        university=university,
        programs=programs,
        scholarships=scholarships_list,
        faqs=faqs,
        placement_partners=placement_partners,
        top_recruiters=top_recruiters,
        similar_universities=similar_universities,
        avatar=_avatar_initials(university.name),
        is_saved=is_saved,
    )


# ---------------------------------------------------------------------------
# /program/<slug> — Database-driven Program Details Page
# ---------------------------------------------------------------------------

_PROGRAM_EMOJI = {
    "MBA":    "🎓",
    "MCA":    "💻",
    "BCA":    "🖥️",
    "BBA":    "📊",
    "B.Tech": "⚙️",
    "M.Tech": "🔬",
}


def _get_related_programs(program, limit=4):
    """
    Return up to `limit` related Program objects (as plain dicts).

    Priority:
      1. Same university, different program.
      2. Same category (any university), excluding current.
    Only active programs are considered.
    """
    from sqlalchemy.orm import joinedload  # already imported at top, safe to re-ref

    same_uni = []
    if program.university_id:
        same_uni = (
            Program.query
            .filter(
                Program.is_active.is_(True),
                Program.university_id == program.university_id,
                Program.id != program.id,
            )
            .options(
                joinedload(Program.university),
                joinedload(Program.category),
                joinedload(Program.specialization),
            )
            .limit(limit)
            .all()
        )

    remaining = limit - len(same_uni)
    same_cat = []
    if remaining > 0 and program.category_id:
        exclude_ids = {program.id} | {p.id for p in same_uni}
        same_cat = (
            Program.query
            .filter(
                Program.is_active.is_(True),
                Program.category_id == program.category_id,
                ~Program.id.in_(exclude_ids),
            )
            .options(
                joinedload(Program.university),
                joinedload(Program.category),
                joinedload(Program.specialization),
            )
            .limit(remaining)
            .all()
        )

    results = []
    for p in same_uni + same_cat:
        cat_name = p.category.name if p.category else None
        results.append({
            "slug":         p.slug,
            "title":        p.title,
            "university":   p.university.name if p.university else None,
            "category":     cat_name,
            "specialization": p.specialization.name if p.specialization else None,
            "duration":     p.duration,
            "fees":         float(p.fees) if p.fees is not None else None,
            "mode":         p.mode,
            "emoji":        _PROGRAM_EMOJI.get(cat_name, "🎓"),
        })
    return results


@main_bp.route("/program/<slug>")
def program_detail(slug):
    """
    Fully database-driven Program Details Page.

    Loads the program with its university, category, and specialization
    in a single eager-loaded query. Derives 4 related programs (same
    university first, then same category). 404s for unknown or inactive
    slugs.
    """
    program = (
        Program.query
        .filter_by(slug=slug, is_active=True)
        .options(
            joinedload(Program.university).joinedload(University.programs)
                .joinedload(Program.category),
            joinedload(Program.university).joinedload(University.programs)
                .joinedload(Program.specialization),
            joinedload(Program.category),
            joinedload(Program.specialization),
        )
        .first_or_404()
    )

    university    = program.university
    category      = program.category
    specialization = program.specialization

    related_programs = _get_related_programs(program)

    uni_avatar = _avatar_initials(university.name) if university else ""

    # Phase 7C-1: has the current user saved this program?
    is_saved = False
    if session.get("user_id"):
        is_saved = SavedProgram.query.filter_by(
            user_id=session["user_id"],
            program_id=program.id,
        ).first() is not None

    # Phase 7C-2: record recently-viewed
    if session.get("user_id"):
        try:
            _record_recently_viewed(
                user_id=session["user_id"],
                university_id=None,
                program_id=program.id,
            )
        except Exception:
            db.session.rollback()

    return render_template(
        "program_details.html",
        program=program,
        university=university,
        category=category,
        specialization=specialization,
        related_programs=related_programs,
        uni_avatar=uni_avatar,
        is_saved=is_saved,
    )


# ---------------------------------------------------------------------------
# Authentication (merged from the former routes/auth.py)
# ---------------------------------------------------------------------------
# Uses the existing User model (models/user.py) exactly as-is — password
# hashing/verification goes through User.set_password() / User.check_password();
# no new columns, no schema changes. Session-based auth: on success we store
# the user's primary key in the signed Flask session (session["user_id"]);
# no server-side session store or new tables required.


@main_bp.app_context_processor
def inject_current_user():
    """
    Expose `current_user` to all Jinja templates.

    Returns the logged-in User row for the id stored in the session, or
    None if there is no session / the session is stale (e.g. the user
    was deactivated or deleted after logging in) — in the stale case the
    dangling session is cleared so subsequent requests don't re-query.
    """
    user_id = session.get("user_id")
    if not user_id:
        return {"current_user": None}

    user = User.query.get(user_id)
    if user is None or not user.is_active:
        session.pop("user_id", None)
        return {"current_user": None}

    return {"current_user": user}


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("main.index"))

    if request.method == "POST":
        full_name = (request.form.get("full_name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        mobile = _digits_only(request.form.get("mobile"))
        password = request.form.get("password") or ""
        confirm_password = request.form.get("confirm_password") or ""

        errors = []

        if len(full_name) < 2:
            errors.append("Please enter your full name (at least 2 characters).")

        if not EMAIL_RE.match(email):
            errors.append("Please enter a valid email address.")

        if len(mobile) != 10:
            errors.append("Please enter a valid 10-digit mobile number.")

        if len(password) < MIN_PASSWORD_LENGTH:
            errors.append(
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
            )

        if password != confirm_password:
            errors.append("Passwords do not match.")

        # Uniqueness checks only run once the basic field checks pass —
        # no point hitting the DB for an already-invalid submission.
        if not errors and User.query.filter_by(email=email).first():
            errors.append("An account with this email already exists.")

        if not errors and User.query.filter_by(mobile=mobile).first():
            errors.append("An account with this mobile number already exists.")

        if errors:
            for message in errors:
                flash(message, "error")
            return (
                render_template(
                    "register.html",
                    full_name=full_name,
                    email=email,
                    mobile=mobile,
                ),
                400,
            )

        user = User(
            full_name=full_name,
            email=email,
            mobile=mobile,
            is_verified=False,
            is_admin=False,
            is_active=True,
        )
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Could not create your account. Please try again.", "error")
            return (
                render_template(
                    "register.html",
                    full_name=full_name,
                    email=email,
                    mobile=mobile,
                ),
                500,
            )

        session.clear()
        session["user_id"] = user.id
        flash("Welcome to Campus Unlock! Your account has been created.", "success")
        return redirect(url_for("main.index"))

    return render_template("register.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return render_template("login.html", email=email), 401

        if not user.is_active:
            flash(
                "This account has been deactivated. Please contact support.",
                "error",
            )
            return render_template("login.html", email=email), 403

        session.clear()
        session["user_id"] = user.id

        user.last_login = datetime.utcnow()
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

        flash(f"Welcome back, {user.full_name.split(' ')[0]}!", "success")

        # Phase 8A: role-based landing. An explicit ?next= (e.g. from
        # login_required/admin_required bouncing an anonymous visit)
        # still wins, preserving existing redirect-back behavior.
        next_url = request.args.get("next")
        if next_url:
            return redirect(next_url)

        if user.is_admin_role():
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@main_bp.route("/profile")
def profile():
    """Read-only — required by the navbar's 'Profile' link; no CRUD."""
    if not session.get("user_id"):
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("main.login", next=request.path))

    return render_template("profile.html")


@main_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You've been logged out.", "success")
    return redirect(url_for("main.index"))


# ---------------------------------------------------------------------------
# Student Dashboard
# ---------------------------------------------------------------------------
# Read-only profile summary + "My Enquiries" (the logged-in user's own Lead
# records) + self-service Edit Profile / Change Password. No admin surface,
# no arbitrary CRUD, no schema changes.
#
# Leads have no user_id column (see models/lead.py — by design, leads are
# plain-text captures, not FK'd to University/Program yet). The only
# reliable existing link between a Lead and a User is email, so "My
# Enquiries" matches Lead.email == current user's email. This is a
# query-time join only; nothing about the leads table is altered.


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Student dashboard: profile summary, enquiry history, and the
    edit-profile / change-password forms all live on this one page.

    Phase 7C-1 additions
    --------------------
    saved_universities  — user's bookmarked universities (eager-loaded)
    saved_programs      — user's bookmarked programs (eager-loaded)
    """
    user = User.query.get(session["user_id"])

    leads = []
    if user and user.email:
        leads = (
            Lead.query.filter_by(email=user.email)
            .order_by(Lead.created_at.desc())
            .all()
        )

    # Eager-load university/program in the same query — no N+1.
    saved_universities = (
        SavedUniversity.query
        .filter_by(user_id=user.id)
        .options(joinedload(SavedUniversity.university))
        .order_by(SavedUniversity.created_at.desc())
        .all()
    )

    saved_programs = (
        SavedProgram.query
        .filter_by(user_id=user.id)
        .options(
            joinedload(SavedProgram.program).joinedload(Program.university),
            joinedload(SavedProgram.program).joinedload(Program.category),
        )
        .order_by(SavedProgram.created_at.desc())
        .all()
    )

    # Phase 7C-2: recently viewed universities
    recent_universities = (
        RecentlyViewed.query
        .filter_by(user_id=user.id)
        .filter(RecentlyViewed.university_id.isnot(None))
        .options(joinedload(RecentlyViewed.university))
        .order_by(RecentlyViewed.viewed_at.desc())
        .limit(10)
        .all()
    )

    # Phase 7C-2: recently viewed programs
    recent_programs = (
        RecentlyViewed.query
        .filter_by(user_id=user.id)
        .filter(RecentlyViewed.program_id.isnot(None))
        .options(
            joinedload(RecentlyViewed.program).joinedload(Program.university),
            joinedload(RecentlyViewed.program).joinedload(Program.category),
        )
        .order_by(RecentlyViewed.viewed_at.desc())
        .limit(10)
        .all()
    )

    # Phase 7C-2: compare history (newest 5)
    compare_history = (
        CompareHistory.query
        .filter_by(user_id=user.id)
        .order_by(CompareHistory.compared_at.desc())
        .limit(5)
        .all()
    )

    # Phase 7C-2: brochure downloads (newest 10)
    brochure_history = (
        BrochureDownload.query
        .filter_by(user_id=user.id)
        .options(
            joinedload(BrochureDownload.university),
            joinedload(BrochureDownload.program).joinedload(Program.university),
        )
        .order_by(BrochureDownload.downloaded_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard.html",
        leads=leads,
        saved_universities=saved_universities,
        saved_programs=saved_programs,
        recent_universities=recent_universities,
        recent_programs=recent_programs,
        compare_history=compare_history,
        brochure_history=brochure_history,
    )


@main_bp.route("/dashboard/profile", methods=["POST"])
@login_required
def update_profile():
    """
    Edit Profile — Name and Mobile Number only. Email is intentionally
    not editable here (email is the account identifier and the join key
    used for "My Enquiries").
    """
    user = User.query.get(session["user_id"])

    full_name = (request.form.get("full_name") or "").strip()
    mobile = _digits_only(request.form.get("mobile"))

    errors = []

    if len(full_name) < 2:
        errors.append("Please enter your full name (at least 2 characters).")

    if len(mobile) != 10:
        errors.append("Please enter a valid 10-digit mobile number.")

    if not errors and mobile != user.mobile:
        existing = User.query.filter_by(mobile=mobile).first()
        if existing and existing.id != user.id:
            errors.append("An account with this mobile number already exists.")

    if errors:
        for message in errors:
            flash(message, "error")
        return redirect(url_for("main.dashboard"))

    user.full_name = full_name
    user.mobile = mobile

    try:
        db.session.commit()
        flash("Your profile has been updated.", "success")
    except Exception:
        db.session.rollback()
        flash("Could not update your profile. Please try again.", "error")

    return redirect(url_for("main.dashboard"))


@main_bp.route("/dashboard/password", methods=["POST"])
@login_required
def change_password():
    """Change Password — requires the current password to be re-entered."""
    user = User.query.get(session["user_id"])

    current_password = request.form.get("current_password") or ""
    new_password = request.form.get("new_password") or ""
    confirm_new_password = request.form.get("confirm_new_password") or ""

    errors = []

    if not user.check_password(current_password):
        errors.append("Current password is incorrect.")

    if len(new_password) < MIN_PASSWORD_LENGTH:
        errors.append(
            f"New password must be at least {MIN_PASSWORD_LENGTH} characters long."
        )

    if new_password != confirm_new_password:
        errors.append("New passwords do not match.")

    if errors:
        for message in errors:
            flash(message, "error")
        return redirect(url_for("main.dashboard"))

    user.set_password(new_password)

    try:
        db.session.commit()
        flash("Your password has been changed.", "success")
    except Exception:
        db.session.rollback()
        flash("Could not change your password. Please try again.", "error")

    return redirect(url_for("main.dashboard"))


# ---------------------------------------------------------------------------
# Phase 7C-1 — Saved Universities & Programs
# ---------------------------------------------------------------------------
# All endpoints are POST-only, require login, and return JSON so the frontend
# can toggle the button state without a page reload.
# Shape on success: { "saved": true|false }
#
# Security: user_id is always read from the server-side session — never from
# the request body — so users can never touch another user's saved items.
# ---------------------------------------------------------------------------

@main_bp.route("/save/university/<int:university_id>", methods=["POST"])
@login_required
def toggle_save_university(university_id):
    """
    Toggle the saved state of a university for the current user.

    POST /save/university/<id>
    Returns 200 { "saved": bool }
    Returns 404 if university does not exist / is inactive.
    Returns 500 { "error": "..." } on DB failure.
    """
    user_id = session["user_id"]

    university = University.query.filter_by(
        id=university_id, is_active=True
    ).first_or_404()

    existing = SavedUniversity.query.filter_by(
        user_id=user_id, university_id=university.id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({"saved": False})

    row = SavedUniversity(user_id=user_id, university_id=university.id)
    try:
        db.session.add(row)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not save. Please try again."}), 500

    return jsonify({"saved": True})


@main_bp.route("/save/program/<int:program_id>", methods=["POST"])
@login_required
def toggle_save_program(program_id):
    """
    Toggle the saved state of a program for the current user.

    POST /save/program/<id>
    Returns 200 { "saved": bool }
    Returns 404 if program does not exist / is inactive.
    Returns 500 { "error": "..." } on DB failure.
    """
    user_id = session["user_id"]

    program = Program.query.filter_by(
        id=program_id, is_active=True
    ).first_or_404()

    existing = SavedProgram.query.filter_by(
        user_id=user_id, program_id=program.id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({"saved": False})

    row = SavedProgram(user_id=user_id, program_id=program.id)
    try:
        db.session.add(row)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not save. Please try again."}), 500

    return jsonify({"saved": True})


# ---------------------------------------------------------------------------
# Phase 7C-2 — Brochure Download Tracker
# ---------------------------------------------------------------------------

@main_bp.route("/brochure/track", methods=["POST"])
@login_required
def track_brochure():
    """
    POST /brochure/track

    Body (JSON): { "university_id": <int|null>, "program_id": <int|null> }

    Records a brochure download event and returns the brochure URL so the
    frontend can open it in a new tab.

    At least one of university_id / program_id must be provided.
    The URL is resolved server-side from the DB; the client never crafts it.
    """
    user_id = session["user_id"]
    data = request.get_json(silent=True) or {}

    university_id = data.get("university_id")
    program_id    = data.get("program_id")

    if not university_id and not program_id:
        return jsonify({"error": "university_id or program_id required."}), 400

    brochure_url = None

    if program_id:
        prog = Program.query.filter_by(id=program_id, is_active=True).first()
        if prog:
            brochure_url = prog.brochure
            if not brochure_url and prog.university:
                brochure_url = prog.university.brochure_url

    if not brochure_url and university_id:
        uni = University.query.filter_by(id=university_id, is_active=True).first()
        if uni:
            brochure_url = uni.brochure_url

    try:
        row = BrochureDownload(
            user_id=user_id,
            university_id=university_id if university_id else None,
            program_id=program_id if program_id else None,
        )
        db.session.add(row)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return jsonify({"ok": True, "url": brochure_url})


# ---------------------------------------------------------------------------
# Phase 7C-2 — Clear History
# ---------------------------------------------------------------------------
# Three distinct clear targets: recently_viewed, compare_history,
# brochure_downloads.  Each is a separate POST so the dashboard can offer
# per-section "Clear" buttons without a full page form submission.
# Saved universities/programs are NOT affected by any of these.
# ---------------------------------------------------------------------------

@main_bp.route("/history/clear/<target>", methods=["POST"])
@login_required
def clear_history(target):
    """
    POST /history/clear/<target>
    target: "viewed" | "compare" | "brochure"

    Deletes the specified history table rows belonging to the current user.
    Returns JSON { "ok": true } on success, 400 on unknown target.
    Saved universities/programs are never touched.
    """
    user_id = session["user_id"]

    allowed = {
        "viewed":  RecentlyViewed,
        "compare": CompareHistory,
        "brochure": BrochureDownload,
    }

    model = allowed.get(target)
    if model is None:
        return jsonify({"error": f"Unknown target '{target}'."}), 400

    try:
        model.query.filter_by(user_id=user_id).delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not clear history. Please try again."}), 500

    return jsonify({"ok": True})
