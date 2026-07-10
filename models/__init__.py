"""
Campus Unlock — Database Extensions
================================
This module only initializes the shared SQLAlchemy and Migrate
extension instances. They are bound to the Flask app via
db.init_app(app) / migrate.init_app(app, db) inside the application
factory (app.py).

No models are defined here yet — this is the database foundation
only, so `flask db init/migrate/upgrade` can be run later once
models exist.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from .university import University
from .category import Category
from .specialization import Specialization
from .program import Program

from .user import User
from .lead import Lead