"""
Campus Unlock — Admin Blueprint (Phase 8B: Full CRUD)
======================================================
All routes render admin/dashboard.html with a `view` variable that
controls which section is shown — no new template files are created.

view values
-----------
  "dashboard"           — default overview (unchanged from 8A)
  "universities"        — list
  "university_form"     — create / edit form
  "programs"            — list
  "program_form"        — create / edit form
  "leads"               — list
  "lead_detail"         — single lead read-only + status update
  "users"               — list
  "user_detail"         — single user read-only
  "brochure_downloads"  — list

All writes use POST only. A lightweight session-based CSRF token is
validated on every mutating request.
"""

import re
import secrets
import unicodedata
from datetime import datetime

from flask import (
    Blueprint, abort, flash, redirect, render_template,
    request, session, url_for,
)
from sqlalchemy import func, or_


def slugify(text):
    """Pure-stdlib slug generator — no external dependency needed."""
    text = unicodedata.normalize("NFKD", str(text))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "item"

from routes.main import admin_required
from models import db, University, Program
from models.user import User
from models.lead import Lead
from models.history import BrochureDownload

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

PAGE_SIZE    = 20
LEAD_STATUSES = ["New", "Contacted", "Qualified", "Converted", "Closed"]
OWNERSHIP_CHOICES = ["Private", "Government", "Deemed", "Autonomous"]
UNIV_TYPE_CHOICES = [
    "Central University", "State University", "Deemed-to-be University",
    "Private University", "Autonomous Institution",
]


# ---------------------------------------------------------------------------
# CSRF helpers
# ---------------------------------------------------------------------------

def _csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def _validate_csrf():
    token = request.form.get("csrf_token", "")
    if not token or token != session.get("csrf_token"):
        abort(400, "Invalid CSRF token.")


@admin_bp.before_request
def _ensure_csrf():
    _csrf_token()


@admin_bp.app_context_processor
def _ctx():
    return {"csrf_token": _csrf_token}


# ---------------------------------------------------------------------------
# Slug helper
# ---------------------------------------------------------------------------

def _unique_slug(name, model, exclude_id=None):
    base = slugify(name)
    candidate = base
    n = 1
    while True:
        q = model.query.filter_by(slug=candidate)
        if exclude_id:
            q = q.filter(model.id != exclude_id)
        if not q.first():
            return candidate
        candidate = f"{base}-{n}"
        n += 1


# ---------------------------------------------------------------------------
# Type coercions
# ---------------------------------------------------------------------------

def _int(v):
    try:
        return int(v) if v and str(v).strip() else None
    except (ValueError, TypeError):
        return None


def _float(v):
    try:
        return float(v) if v and str(v).strip() else None
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Shared render helper — every admin view goes through dashboard.html
# ---------------------------------------------------------------------------

def _render(view, **ctx):
    ctx["view"] = view
    ctx.setdefault("q", "")
    return render_template("admin/dashboard.html", **ctx)


# ===========================================================================
# DASHBOARD
# ===========================================================================

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    counts = {
        "users":              User.query.count(),
        "universities":       University.query.count(),
        "programs":           Program.query.count(),
        "leads":              Lead.query.count(),
        "brochure_downloads": BrochureDownload.query.count(),
    }
    recent_leads = Lead.query.order_by(Lead.created_at.desc()).limit(6).all()
    top_universities = (
        db.session.query(University, func.count(Program.id).label("program_count"))
        .outerjoin(Program, Program.university_id == University.id)
        .group_by(University.id)
        .order_by(func.count(Program.id).desc(), University.name.asc())
        .limit(5).all()
    )
    recent_programs  = Program.query.order_by(Program.created_at.desc()).limit(6).all()
    recent_downloads = BrochureDownload.query.order_by(BrochureDownload.downloaded_at.desc()).limit(5).all()

    activity = []
    for lead in Lead.query.order_by(Lead.created_at.desc()).limit(8).all():
        activity.append({"type": "lead", "at": lead.created_at,
                         "title": f"New lead — {lead.full_name}",
                         "detail": lead.interested_program or lead.interested_university})
    for dl in recent_downloads:
        target = dl.university.name if dl.university else (dl.program.title if dl.program else "brochure")
        activity.append({"type": "download", "at": dl.downloaded_at,
                         "title": "Brochure downloaded", "detail": target})
    for user in User.query.order_by(User.created_at.desc()).limit(5).all():
        activity.append({"type": "signup", "at": user.created_at,
                         "title": f"New user signed up — {user.full_name}",
                         "detail": user.email})
    activity.sort(key=lambda x: x["at"], reverse=True)

    return _render("dashboard",
        counts=counts, recent_leads=recent_leads,
        top_universities=top_universities, recent_programs=recent_programs,
        recent_downloads=recent_downloads, activity=activity[:8])


# ===========================================================================
# UNIVERSITIES — list
# ===========================================================================

@admin_bp.route("/universities")
@admin_required
def universities():
    q      = request.args.get("q", "").strip()
    status = request.args.get("status", "all")
    page   = max(1, request.args.get("page", 1, type=int))

    query = University.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            University.name.ilike(like), University.city.ilike(like),
            University.state.ilike(like), University.accreditation.ilike(like)))
    if status == "active":
        query = query.filter(University.is_active == True)
    elif status == "inactive":
        query = query.filter(University.is_active == False)

    pagination = query.order_by(University.name.asc()).paginate(page=page, per_page=PAGE_SIZE, error_out=False)
    return _render("universities", pagination=pagination, q=q, status=status)


# ===========================================================================
# UNIVERSITIES — new
# ===========================================================================

@admin_bp.route("/universities/new", methods=["GET", "POST"])
@admin_required
def university_new():
    if request.method == "POST":
        _validate_csrf()
        name = request.form.get("name", "").strip()
        if not name:
            flash("University name is required.", "error")
            return _render("university_form", university=None, form=request.form,
                           ownership_choices=OWNERSHIP_CHOICES, type_choices=UNIV_TYPE_CHOICES, action="new")

        u = University(
            name=name,
            slug=_unique_slug(name, University),
            city=request.form.get("city","").strip() or None,
            state=request.form.get("state","").strip() or None,
            country=request.form.get("country","").strip() or None,
            website=request.form.get("website","").strip() or None,
            email=request.form.get("email","").strip() or None,
            phone=request.form.get("phone","").strip() or None,
            address=request.form.get("address","").strip() or None,
            accreditation=request.form.get("accreditation","").strip() or None,
            ranking=_int(request.form.get("ranking")),
            established_year=_int(request.form.get("established_year")),
            ownership=request.form.get("ownership") or None,
            university_type=request.form.get("university_type") or None,
            short_description=request.form.get("short_description","").strip() or None,
            full_description=request.form.get("full_description","").strip() or None,
            why_choose=request.form.get("why_choose","").strip() or None,
            logo=request.form.get("logo","").strip() or None,
            logo_url=request.form.get("logo_url","").strip() or None,
            banner_url=request.form.get("banner_url","").strip() or None,
            brochure_url=request.form.get("brochure_url","").strip() or None,
            ugc_approved=bool(request.form.get("ugc_approved")),
            aicte_approved=bool(request.form.get("aicte_approved")),
            aiu_member=bool(request.form.get("aiu_member")),
            wes_approved=bool(request.form.get("wes_approved")),
            placement_support=bool(request.form.get("placement_support")),
            highest_package=_float(request.form.get("highest_package")),
            average_package=_float(request.form.get("average_package")),
            top_recruiters=request.form.get("top_recruiters","").strip() or None,
            total_students=_int(request.form.get("total_students")),
            faculty_count=_int(request.form.get("faculty_count")),
            alumni_count=_int(request.form.get("alumni_count")),
            meta_title=request.form.get("meta_title","").strip() or None,
            meta_description=request.form.get("meta_description","").strip() or None,
            is_active=bool(request.form.get("is_active")),
        )
        db.session.add(u)
        db.session.commit()
        flash(f'University "{u.name}" created.', "success")
        return redirect(url_for("admin.universities"))

    return _render("university_form", university=None, form={},
                   ownership_choices=OWNERSHIP_CHOICES, type_choices=UNIV_TYPE_CHOICES, action="new")


# ===========================================================================
# UNIVERSITIES — edit
# ===========================================================================

@admin_bp.route("/universities/<int:uid>/edit", methods=["GET", "POST"])
@admin_required
def university_edit(uid):
    u = University.query.get_or_404(uid)

    if request.method == "POST":
        _validate_csrf()
        name = request.form.get("name", "").strip()
        if not name:
            flash("University name is required.", "error")
            return _render("university_form", university=u, form=request.form,
                           ownership_choices=OWNERSHIP_CHOICES, type_choices=UNIV_TYPE_CHOICES, action="edit")

        u.name=name; u.city=request.form.get("city","").strip() or None
        u.state=request.form.get("state","").strip() or None
        u.country=request.form.get("country","").strip() or None
        u.website=request.form.get("website","").strip() or None
        u.email=request.form.get("email","").strip() or None
        u.phone=request.form.get("phone","").strip() or None
        u.address=request.form.get("address","").strip() or None
        u.accreditation=request.form.get("accreditation","").strip() or None
        u.ranking=_int(request.form.get("ranking"))
        u.established_year=_int(request.form.get("established_year"))
        u.ownership=request.form.get("ownership") or None
        u.university_type=request.form.get("university_type") or None
        u.short_description=request.form.get("short_description","").strip() or None
        u.full_description=request.form.get("full_description","").strip() or None
        u.why_choose=request.form.get("why_choose","").strip() or None
        u.logo=request.form.get("logo","").strip() or None
        u.logo_url=request.form.get("logo_url","").strip() or None
        u.banner_url=request.form.get("banner_url","").strip() or None
        u.brochure_url=request.form.get("brochure_url","").strip() or None
        u.ugc_approved=bool(request.form.get("ugc_approved"))
        u.aicte_approved=bool(request.form.get("aicte_approved"))
        u.aiu_member=bool(request.form.get("aiu_member"))
        u.wes_approved=bool(request.form.get("wes_approved"))
        u.placement_support=bool(request.form.get("placement_support"))
        u.highest_package=_float(request.form.get("highest_package"))
        u.average_package=_float(request.form.get("average_package"))
        u.top_recruiters=request.form.get("top_recruiters","").strip() or None
        u.total_students=_int(request.form.get("total_students"))
        u.faculty_count=_int(request.form.get("faculty_count"))
        u.alumni_count=_int(request.form.get("alumni_count"))
        u.meta_title=request.form.get("meta_title","").strip() or None
        u.meta_description=request.form.get("meta_description","").strip() or None
        u.is_active=bool(request.form.get("is_active"))
        u.updated_at=datetime.utcnow()
        db.session.commit()
        flash(f'University "{u.name}" updated.', "success")
        return redirect(url_for("admin.universities"))

    return _render("university_form", university=u, form={},
                   ownership_choices=OWNERSHIP_CHOICES, type_choices=UNIV_TYPE_CHOICES, action="edit")


# ===========================================================================
# UNIVERSITIES — delete
# ===========================================================================

@admin_bp.route("/universities/<int:uid>/delete", methods=["POST"])
@admin_required
def university_delete(uid):
    _validate_csrf()
    u = University.query.get_or_404(uid)
    name = u.name
    db.session.delete(u)
    db.session.commit()
    flash(f'University "{name}" deleted.', "success")
    return redirect(url_for("admin.universities"))


# ===========================================================================
# PROGRAMS — list
# ===========================================================================

@admin_bp.route("/programs")
@admin_required
def programs():
    q      = request.args.get("q", "").strip()
    uni_id = request.args.get("university_id", "")
    status = request.args.get("status", "all")
    page   = max(1, request.args.get("page", 1, type=int))

    query = Program.query.join(University, Program.university_id == University.id)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            Program.title.ilike(like), Program.mode.ilike(like),
            University.name.ilike(like)))
    if uni_id.isdigit():
        query = query.filter(Program.university_id == int(uni_id))
    if status == "active":
        query = query.filter(Program.is_active == True)
    elif status == "inactive":
        query = query.filter(Program.is_active == False)

    pagination = query.order_by(Program.created_at.desc()).paginate(page=page, per_page=PAGE_SIZE, error_out=False)
    all_universities = University.query.order_by(University.name).all()
    return _render("programs", pagination=pagination, q=q, uni_id=uni_id,
                   status=status, all_universities=all_universities)


# ===========================================================================
# PROGRAMS — new
# ===========================================================================

@admin_bp.route("/programs/new", methods=["GET", "POST"])
@admin_required
def program_new():
    all_universities = University.query.order_by(University.name).all()

    if request.method == "POST":
        _validate_csrf()
        title  = request.form.get("title","").strip()
        uni_id = request.form.get("university_id","").strip()
        if not title or not uni_id:
            flash("Title and university are required.", "error")
            return _render("program_form", program=None, form=request.form,
                           all_universities=all_universities, action="new")

        p = Program(
            university_id=int(uni_id),
            category_id=_int(request.form.get("category_id")) or 1,
            title=title,
            slug=_unique_slug(title, Program),
            duration=request.form.get("duration","").strip() or None,
            fees=_float(request.form.get("fees")),
            eligibility=request.form.get("eligibility","").strip() or None,
            mode=request.form.get("mode","").strip() or None,
            brochure=request.form.get("brochure","").strip() or None,
            description=request.form.get("description","").strip() or None,
            is_featured=bool(request.form.get("is_featured")),
            is_active=bool(request.form.get("is_active")),
        )
        db.session.add(p)
        db.session.commit()
        flash(f'Program "{p.title}" created.', "success")
        return redirect(url_for("admin.programs"))

    return _render("program_form", program=None, form={},
                   all_universities=all_universities, action="new")


# ===========================================================================
# PROGRAMS — edit
# ===========================================================================

@admin_bp.route("/programs/<int:pid>/edit", methods=["GET", "POST"])
@admin_required
def program_edit(pid):
    p = Program.query.get_or_404(pid)
    all_universities = University.query.order_by(University.name).all()

    if request.method == "POST":
        _validate_csrf()
        title  = request.form.get("title","").strip()
        uni_id = request.form.get("university_id","").strip()
        if not title or not uni_id:
            flash("Title and university are required.", "error")
            return _render("program_form", program=p, form=request.form,
                           all_universities=all_universities, action="edit")

        p.university_id=int(uni_id); p.title=title
        p.duration=request.form.get("duration","").strip() or None
        p.fees=_float(request.form.get("fees"))
        p.eligibility=request.form.get("eligibility","").strip() or None
        p.mode=request.form.get("mode","").strip() or None
        p.brochure=request.form.get("brochure","").strip() or None
        p.description=request.form.get("description","").strip() or None
        p.is_featured=bool(request.form.get("is_featured"))
        p.is_active=bool(request.form.get("is_active"))
        p.updated_at=datetime.utcnow()
        db.session.commit()
        flash(f'Program "{p.title}" updated.', "success")
        return redirect(url_for("admin.programs"))

    return _render("program_form", program=p, form={},
                   all_universities=all_universities, action="edit")


# ===========================================================================
# PROGRAMS — delete
# ===========================================================================

@admin_bp.route("/programs/<int:pid>/delete", methods=["POST"])
@admin_required
def program_delete(pid):
    _validate_csrf()
    p = Program.query.get_or_404(pid)
    title = p.title
    db.session.delete(p)
    db.session.commit()
    flash(f'Program "{title}" deleted.', "success")
    return redirect(url_for("admin.programs"))


# ===========================================================================
# LEADS — list
# ===========================================================================

@admin_bp.route("/leads")
@admin_required
def leads():
    q      = request.args.get("q", "").strip()
    status = request.args.get("status", "all")
    page   = max(1, request.args.get("page", 1, type=int))

    query = Lead.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            Lead.full_name.ilike(like), Lead.email.ilike(like),
            Lead.mobile.ilike(like), Lead.interested_university.ilike(like),
            Lead.interested_program.ilike(like)))
    if status != "all":
        query = query.filter(Lead.status == status)

    pagination = query.order_by(Lead.created_at.desc()).paginate(page=page, per_page=PAGE_SIZE, error_out=False)
    return _render("leads", pagination=pagination, q=q, status=status, lead_statuses=LEAD_STATUSES)


# ===========================================================================
# LEADS — detail + status update
# ===========================================================================

@admin_bp.route("/leads/<int:lid>")
@admin_required
def lead_detail(lid):
    lead = Lead.query.get_or_404(lid)
    return _render("lead_detail", lead=lead, lead_statuses=LEAD_STATUSES)


@admin_bp.route("/leads/<int:lid>/status", methods=["POST"])
@admin_required
def lead_status(lid):
    _validate_csrf()
    lead = Lead.query.get_or_404(lid)
    new_status = request.form.get("status","").strip()
    if new_status not in LEAD_STATUSES:
        abort(400, "Invalid status.")
    lead.status = new_status
    lead.updated_at = datetime.utcnow()
    db.session.commit()
    flash(f'Status updated to "{new_status}".', "success")
    return redirect(url_for("admin.lead_detail", lid=lid))


# ===========================================================================
# USERS — list
# ===========================================================================

@admin_bp.route("/users")
@admin_required
def users():
    q    = request.args.get("q","").strip()
    role = request.args.get("role","all")
    page = max(1, request.args.get("page", 1, type=int))

    query = User.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(User.full_name.ilike(like), User.email.ilike(like)))
    if role != "all":
        query = query.filter(User.role == role)

    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=PAGE_SIZE, error_out=False)
    return _render("users", pagination=pagination, q=q, role=role)


# ===========================================================================
# USERS — detail + active toggle
# ===========================================================================

@admin_bp.route("/users/<int:uid>")
@admin_required
def user_detail(uid):
    user = User.query.get_or_404(uid)
    return _render("user_detail", user=user)


@admin_bp.route("/users/<int:uid>/toggle", methods=["POST"])
@admin_required
def user_toggle(uid):
    _validate_csrf()
    user = User.query.get_or_404(uid)
    user.is_active = not user.is_active
    db.session.commit()
    state = "activated" if user.is_active else "deactivated"
    flash(f'User "{user.full_name}" {state}.', "success")
    return redirect(url_for("admin.users"))


# ===========================================================================
# BROCHURE DOWNLOADS — list
# ===========================================================================

@admin_bp.route("/brochure-downloads")
@admin_required
def brochure_downloads():
    page = max(1, request.args.get("page", 1, type=int))
    pagination = (
        BrochureDownload.query
        .order_by(BrochureDownload.downloaded_at.desc())
        .paginate(page=page, per_page=PAGE_SIZE, error_out=False)
    )
    return _render("brochure_downloads", pagination=pagination)