"""Configuration module for Constellate Flask application.

Defines application settings, database configuration, and security settings.
"""

import os
from pathlib import Path


class Config:
    """Base configuration class for the Flask application.

    Attributes:
        SECRET_KEY: Secret key for session management and CSRF protection
        SQLALCHEMY_DATABASE_URI: Database connection URI
        SQLALCHEMY_TRACK_MODIFICATIONS: Disable SQLAlchemy event system
        WTF_CSRF_ENABLED: Enable CSRF protection for Flask-WTF forms

    """

    # Secret key for session management and CSRF protection
    # In production, this should be set via environment variable
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Database configuration
    # Ensure instance directory exists
    BASE_DIR = Path(__file__).parent
    INSTANCE_DIR = BASE_DIR / "instance"
    INSTANCE_DIR.mkdir(exist_ok=True)

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f'sqlite:///{INSTANCE_DIR / "site.db"}'

    # Disable SQLAlchemy event system for performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-WTF configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens

