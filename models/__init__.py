"""
Campus Unlock — Database Extensions
================================
Initializes the shared SQLAlchemy and Flask-Migrate extension instances.
They are bound to the Flask app via db.init_app(app) / migrate.init_app(app, db)
inside the application factory (app.py).

Import order matters for SQLAlchemy's relationship resolution:
  1. Extension instances first (db, migrate)
  2. Models with no FK dependencies (University, Category)
  3. Models that depend on the above (Specialization → Category,
     Program → University + Category + Specialization)
  4. New child models that depend on University
     (Scholarship, FAQ, PlacementPartner)
  5. Stand-alone user-facing models (User, Lead)
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Core domain models
from .university import University
from .category import Category
from .specialization import Specialization
from .program import Program

# New production models (children of University)
from .scholarship import Scholarship
from .faq import FAQ
from .placement_partner import PlacementPartner

# User / lead models (unchanged)
from .user import User
from models.lead import Lead

# Phase 7C-1 — saved items
from .saved import SavedUniversity, SavedProgram

# Phase 7C-2 — user history
from .history import RecentlyViewed, CompareHistory, BrochureDownload

# Phase 9 — CMS & Content (homepage content + site-wide SEO key/value store)
from .site_content import SiteContent

# Password reset — single-use hashed tokens with expiry (forgot-password flow)
from .password_reset_token import PasswordResetToken
