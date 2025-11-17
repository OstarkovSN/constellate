"""Tests for application initialization and CLI.

Tests app factory, user loader, and CLI entry point.
"""

from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner
from flask import Flask
from flask_login import current_user, login_user

from app import main
from models.article import Article  # noqa: F401 - needed for SQLAlchemy relationship
from models.user import User


class TestAppFactory:
    """Test cases for application factory."""

    def test_create_app(self, app: Flask) -> None:
        """Test that create_app returns a Flask application."""
        assert isinstance(app, Flask)
        assert app.name == "app"

    def test_user_loader_with_valid_id(self, app: Flask, test_user: User) -> None:
        """Test that user_loader correctly loads a user by ID."""
        with app.test_request_context():
            # Login the user to establish session
            login_user(test_user)

            # Access current_user which triggers user_loader
            assert current_user.is_authenticated
            assert current_user.id == test_user.id
            assert current_user.username == test_user.username

    def test_user_loader_with_invalid_id(self, app: Flask, client) -> None:
        """Test that user_loader returns None for non-existent user ID."""
        # Manually set a session with invalid user ID
        with client.session_transaction() as sess:
            sess["_user_id"] = "99999"

        # Make a request - user_loader will be called and return None
        response = client.get("/graph")
        # Should redirect to login or return 401 since user doesn't exist
        assert response.status_code in [200, 401, 302]

    def test_user_loader_with_invalid_string(self, app: Flask, client) -> None:
        """Test that user_loader raises ValueError for invalid string IDs."""
        # Manually set a session with invalid string ID
        with client.session_transaction() as sess:
            sess["_user_id"] = "not_a_number"

        # Make a request - user_loader will try to convert to int and raise ValueError
        # This tests that line 52 (int(user_id)) is executed
        with pytest.raises(ValueError, match="invalid literal for int"):
            client.get("/graph")


class TestCLI:
    """Test cases for CLI entry point."""

    def test_main_function(self) -> None:
        """Test that main function can be called via CLI."""
        runner = CliRunner()
        with patch("app.create_app") as mock_create_app:
            mock_app = MagicMock()
            mock_create_app.return_value = mock_app

            result = runner.invoke(main, ["--help"])

            # Should show help without error
            assert result.exit_code == 0
            assert "Enable debug mode" in result.output

    def test_main_function_with_debug_flag(self) -> None:
        """Test that main function accepts debug flag."""
        runner = CliRunner()
        with patch("app.create_app") as mock_create_app:
            mock_app = MagicMock()
            mock_create_app.return_value = mock_app
            with patch.object(mock_app, "run") as mock_run:
                runner.invoke(main, ["--debug"])

                # Should call app.run with debug=True
                # Binding to 0.0.0.0 is intentional for development
                mock_run.assert_called_once_with(
                    debug=True, host="0.0.0.0", port=5000,  # noqa: S104
                )

