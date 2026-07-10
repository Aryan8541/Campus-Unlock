"""
Campus Unlock — Main Blueprint
==========================
Houses the home route and placeholder routes for pages that don't
exist yet. Placeholders return a lightweight "Coming Soon" response
(HTTP 501) instead of crashing, so nav links and future frontend work
never hit a raw 404/500 during development.
"""

from flask import Blueprint, render_template, render_template_string

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


def _coming_soon(page_name):
    """Render a minimal inline 'Coming Soon' page with a 501 status."""
    return render_template_string(_COMING_SOON_TEMPLATE, page_name=page_name), 501


@main_bp.route("/")
def index():
    """Home page."""
    return render_template("index.html")


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
