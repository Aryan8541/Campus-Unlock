"""
Campus Unlock — Configuration
==========================
Environment-driven configuration classes for the Flask application
factory. Values are sourced from the process environment (populated
via python-dotenv from a local .env file), with safe, non-secret
defaults for local development only.
"""

import os
from dotenv import load_dotenv

# Load variables from a .env file in the project root, if present.
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration shared by all environments."""

    # ------------------------------------------------------------------
    # Core / Security
    # ------------------------------------------------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # ------------------------------------------------------------------
    # Database (SQLAlchemy / SQLite)
    # ------------------------------------------------------------------
    SQLITE_DB_PATH = os.path.join(
        BASE_DIR, "instance", os.environ.get("SQLITE_DB_NAME", "campus_unlock.db")
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # ------------------------------------------------------------------
    # File Uploads
    # ------------------------------------------------------------------
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", os.path.join(BASE_DIR, "static", "images", "uploads")
    )
    MAX_CONTENT_LENGTH = int(
        os.environ.get("MAX_CONTENT_LENGTH", 5 * 1024 * 1024)  # 5 MB default
    )
    ALLOWED_UPLOAD_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "pdf"}

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_FOLDER = os.environ.get("LOG_FOLDER", os.path.join(BASE_DIR, "logs"))
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    # ------------------------------------------------------------------
    # Email — Flask-Mail
    # All values come from environment variables; nothing is hardcoded.
    # For Render (production): set these in the service's Environment tab.
    # For local dev: add them to your .env file.
    # ------------------------------------------------------------------
    MAIL_SERVER   = os.environ.get("MAIL_SERVER",   "smtp.gmail.com")
    MAIL_PORT     = int(os.environ.get("MAIL_PORT",  "587"))
    MAIL_USE_TLS  = os.environ.get("MAIL_USE_TLS",  "true").lower() == "true"
    MAIL_USE_SSL  = os.environ.get("MAIL_USE_SSL",  "false").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        os.environ.get("MAIL_USERNAME", "noreply@campusunlock.in"),
    )

    # ------------------------------------------------------------------
    # Password reset — token lifetime and abuse protection
    # ------------------------------------------------------------------
    RESET_TOKEN_EXPIRY_MINUTES = int(
        os.environ.get("RESET_TOKEN_EXPIRY_MINUTES", "30")
    )
    # Minimum seconds between reset requests for the same email (anti-spam).
    RESET_COOLDOWN_SECONDS = int(
        os.environ.get("RESET_COOLDOWN_SECONDS", "60")
    )
    # Public base URL for building reset links in emails.
    # On Render: set to https://campus-unlock.onrender.com (no trailing slash)
    # Locally: leave blank — the route falls back to request.host_url.
    APP_BASE_URL = os.environ.get("APP_BASE_URL", "")

    # ------------------------------------------------------------------
    # Flags (overridden per-environment below)
    # ------------------------------------------------------------------
    DEBUG = False
    TESTING = False
    ENV = "production"

    @staticmethod
    def init_app(app):
        """Hook for subclasses/environments to run extra setup."""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.LOG_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(Config.SQLITE_DB_PATH), exist_ok=True)


class DevelopmentConfig(Config):
    """Local development configuration."""

    DEBUG = True
    ENV = "development"
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")


class TestingConfig(Config):
    """Configuration used by the automated test suite."""

    TESTING = True
    DEBUG = True
    ENV = "testing"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL", "sqlite:///:memory:"
    )


class ProductionConfig(Config):
    """Production configuration. Assumes SECRET_KEY / DATABASE_URL are set."""

    DEBUG = False
    ENV = "production"

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        if not app.config.get("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY must be set in production.")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
