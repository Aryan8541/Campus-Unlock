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

from flask import Blueprint, render_template, render_template_string, request, jsonify

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload

from models import University, Program, Category, Specialization

main_bp = Blueprint("main", __name__)

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
    """Home page — backed by SQLAlchemy data."""
    data = _load_campus_data()
    return render_template(
        "index.html",
        top_universities=data["top_universities"],
        featured_programs=data["featured_programs"],
        campus_data=data["campus_data"],
    )


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
    return _coming_soon("Compare")


@main_bp.route("/scholarships")
def scholarships():
    return _coming_soon("Scholarships")
