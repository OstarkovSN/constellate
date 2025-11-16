"""Pytest configuration and fixtures for Constellate tests.

Provides shared fixtures for testing the Flask application.
"""

from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from config import Config
from database import db
from models.user import User


class TestConfig(Config):
    """Test configuration class.

    Uses an in-memory SQLite database for faster tests.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    SECRET_KEY = "test-secret-key"


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create and configure a Flask application instance for testing.

    Yields:
        Flask: Configured Flask application instance

    """
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask application.

    Args:
        app: Flask application fixture

    Returns:
        FlaskClient: Test client for making requests

    """
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    """Create a test CLI runner for the Flask application.

    Args:
        app: Flask application fixture

    Returns:
        FlaskCliRunner: CLI test runner

    """
    return app.test_cli_runner()


@pytest.fixture
def test_user(app: Flask) -> User:
    """Create a test user in the database.

    Args:
        app: Flask application fixture

    Returns:
        User: Test user instance

    """
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("testpass123")
        db.session.add(user)
        db.session.commit()

        # Refresh to get the ID
        db.session.refresh(user)
        return user


@pytest.fixture
def authenticated_client(client: FlaskClient, test_user: User) -> FlaskClient:
    """Create a test client with an authenticated user session.

    Args:
        client: Flask test client fixture
        test_user: Test user fixture (ensures user exists before login)

    Returns:
        FlaskClient: Authenticated test client

    """
    # Login the user (test_user ensures user exists in database)
    client.post(
        "/login",
        data={"username": "testuser", "password": "testpass123", "remember_me": False},
        follow_redirects=True,
    )

    return client
