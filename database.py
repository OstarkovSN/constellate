"""Database initialization module.

Handles SQLAlchemy database setup and initialization.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
# This will be initialized with the Flask app in app.py
db = SQLAlchemy()


def init_db() -> None:
    """Initialize database tables.

    Creates all tables defined in the models if they don't already exist.
    Should be called within a Flask application context.
    """
    db.create_all()

