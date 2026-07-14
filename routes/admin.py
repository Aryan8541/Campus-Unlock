"""
Campus Unlock — Admin Blueprint (Phase 8A Foundation)
=======================================================
Scope for this phase, deliberately minimal:
  - Blueprint registration under /admin
  - A single placeholder /admin/dashboard route
  - Reuses admin_required (routes/main.py) for access control

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

from routes.main import admin_required
from models import db, University, Program
from models.user import User
from models.lead import Lead

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """
    Phase 8A placeholder admin dashboard.

    Displays only the label "Admin Dashboard" and four counts
    (Users, Universities, Programs, Leads). No charts, no card
    redesign — reuses the existing design system's section/card
    classes as-is.
    """
    counts = {
        "users": User.query.count(),
        "universities": University.query.count(),
        "programs": Program.query.count(),
        "leads": Lead.query.count(),
    }
    return render_template("admin/dashboard.html", counts=counts)
