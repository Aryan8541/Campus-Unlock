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
