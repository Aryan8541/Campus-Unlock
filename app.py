"""
Campus Unlock — Flask Application Entry Point
==========================================
Application factory for the Campus Unlock platform.

This module is intentionally minimal: it wires together configuration,
templates, static assets, logging, and error handling. Feature routes
are expected to be registered as Blueprints under routes/ as the
project grows (e.g. app.register_blueprint(main_bp)).
"""

import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from config import Config
from models import db, migrate


def create_app(config_class=Config):
    """
    Application factory.

    Using the factory pattern keeps app.py free of hardcoded state,
    makes the app testable, and allows multiple configurations
    (development / testing / production) to be swapped in cleanly.
    """
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    app.config.from_object(config_class)
    app.config.setdefault("SECRET_KEY", os.environ.get("SECRET_KEY"))

    if not app.config.get("SECRET_KEY"):
        # Fail loudly in production; fall back safely only for local dev.
        if app.config.get("ENV") == "production" or not app.debug:
            raise RuntimeError(
                "SECRET_KEY is not set. Define it in your .env file "
                "or environment before starting the application."
            )
        app.config["SECRET_KEY"] = "dev-secret-key-do-not-use-in-production"

    config_class.init_app(app)

    # ------------------------------------------------------------------
    # Database (SQLAlchemy / Migrate)
    # ------------------------------------------------------------------
    db.init_app(app)
    migrate.init_app(app, db)

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    _configure_logging(app)

    # ------------------------------------------------------------------
    # Error handlers
    # ------------------------------------------------------------------
    _register_error_handlers(app)

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    app.logger.info("Campus Unlock application initialized successfully.")
    return app


def _configure_logging(app):
    """Configure console + rotating file logging for the app."""
    log_level = logging.DEBUG if app.debug else logging.INFO

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    app.logger.handlers.clear()
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)

    # Rotating file handler (only if a writable logs directory exists/created)
    try:
        logs_dir = os.path.join(app.root_path, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, "campus_unlock.log"),
            maxBytes=1_000_000,
            backupCount=3,
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)
    except OSError:
        app.logger.warning("Could not create logs directory; file logging disabled.")


def _register_error_handlers(app):
    """Register generic error handlers without depending on new templates."""

    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning("404 Not Found: %s", error)
        return "404 — Page not found.", 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error("500 Internal Server Error: %s", error)
        return "500 — Something went wrong on our end.", 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled exception: %s", error)
        return "500 — Unexpected error.", 500


# ----------------------------------------------------------------------
# Local development entry point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    debug_mode = app.config.get("DEBUG", False)
    app.run(debug=debug_mode)
