"""
Campus Unlock — Admin Blueprint (Phase 8A Foundation)
=======================================================
Scope for this phase:
  - Blueprint registration under /admin
  - A single /admin/dashboard route
  - Reuses admin_required (routes/main.py) for access control

Route, URL prefix, and auth are unchanged from the original 8A
placeholder. The view now additionally queries: recent leads, top
universities (by program count), recently added programs, recent
brochure downloads, and a merged recent-activity feed — all read-only,
no new tables/migrations.

Explicitly OUT of scope for 8A (future phases):
  - CRUD pages, analytics, user management, lead management, forms.

Security
--------
admin_required (imported from routes.main) enforces both:
  1. An active, logged-in session
  2. session user's role == "admin"

Students are never able to reach any view in this blueprint; the
decorator redirects them to their own dashboard instead of leaking
a 403/404 distinction.
"""

from flask import Blueprint, render_template
from sqlalchemy import func

from routes.main import admin_required
from models import db, University, Program
from models.user import User
from models.lead import Lead
from models.history import BrochureDownload

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """
    Admin dashboard: stat counts + Recent Leads, Top Universities,
    Recent Programs Added, and a merged Recent Activity feed.

    All data is read directly from existing tables — no new models,
    no migrations, no writes.
    """
    counts = {
        "users": User.query.count(),
        "universities": University.query.count(),
        "programs": Program.query.count(),
        "leads": Lead.query.count(),
        "brochure_downloads": BrochureDownload.query.count(),
    }

    # ── Recent Leads ────────────────────────────────────────────────
    recent_leads = (
        Lead.query
        .order_by(Lead.created_at.desc())
        .limit(6)
        .all()
    )

    # ── Top Universities (by number of programs offered) ───────────
    top_universities = (
        db.session.query(University, func.count(Program.id).label("program_count"))
        .outerjoin(Program, Program.university_id == University.id)
        .group_by(University.id)
        .order_by(func.count(Program.id).desc(), University.name.asc())
        .limit(5)
        .all()
    )

    # ── Recent Programs Added ───────────────────────────────────────
    recent_programs = (
        Program.query
        .order_by(Program.created_at.desc())
        .limit(6)
        .all()
    )

    # ── Recent Brochure Downloads ────────────────────────────────────
    recent_downloads = (
        BrochureDownload.query
        .order_by(BrochureDownload.downloaded_at.desc())
        .limit(5)
        .all()
    )

    # ── Merged Recent Activity feed (leads + downloads + signups) ───
    activity = []

    for lead in Lead.query.order_by(Lead.created_at.desc()).limit(8).all():
        detail = lead.interested_program or lead.interested_university
        activity.append({
            "type": "lead",
            "at": lead.created_at,
            "title": f"New lead — {lead.full_name}",
            "detail": detail,
        })

    for dl in recent_downloads:
        target = dl.university.name if dl.university else (dl.program.title if dl.program else "brochure")
        activity.append({
            "type": "download",
            "at": dl.downloaded_at,
            "title": "Brochure downloaded",
            "detail": target,
        })

    for user in User.query.order_by(User.created_at.desc()).limit(5).all():
        activity.append({
            "type": "signup",
            "at": user.created_at,
            "title": f"New user signed up — {user.full_name}",
            "detail": user.email,
        })

    activity.sort(key=lambda item: item["at"], reverse=True)
    activity = activity[:8]

    return render_template(
        "admin/dashboard.html",
        counts=counts,
        recent_leads=recent_leads,
        top_universities=top_universities,
        recent_programs=recent_programs,
        recent_downloads=recent_downloads,
        activity=activity,
    )
