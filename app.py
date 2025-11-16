"""Constellate Flask Application.

Main application entry point for the Constellate web application.
Handles initialization of Flask app, database, and routes.
"""


import click
from flask import Flask, Response, abort, redirect, url_for
from flask_login import LoginManager, current_user

from config import Config
from database import db, init_db
from models.user import User
from routes.auth import auth_bp


def create_app(config_class: type[Config] = Config) -> Flask:
    """Application factory pattern for creating Flask app instances.

    Args:
        config_class: Configuration class to use for the application

    Returns:
        Flask: Configured Flask application instance

    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        """Load user by ID for Flask-Login session management.

        Args:
            user_id: String user ID

        Returns:
            User: User object or None if not found

        """
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/")

    # Initialize database tables
    with app.app_context():
        init_db()

    @app.route("/")
    def index() -> Response:
        """Home route that redirects authenticated users to /graph.

        Unauthenticated users are redirected to login.

        Returns:
            Response: Redirect to /graph or /login

        """
        if current_user.is_authenticated:
            return redirect(url_for("graph"))
        return redirect(url_for("auth.login"))

    @app.route("/graph")
    def graph() -> str:
        """Graph visualization route (placeholder for future implementation).

        Requires authentication.

        Returns:
            str: Simple placeholder message

        """
        if not current_user.is_authenticated:
            abort(401)

        return f"<h1>Welcome, {current_user.username}!</h1><p>Graph view coming soon...</p>"

    return app


@click.command()
@click.option("--debug", is_flag=True, help="Enable debug mode")
def main(*, debug: bool = False) -> None:
    """Main entry point for the Constellate Flask application.

    Args:
        debug: Enable Flask debug mode

    """
    app = create_app()
    # Binding to 0.0.0.0 is intentional for development
    app.run(debug=debug, host="0.0.0.0", port=5000)  # noqa: S104


if __name__ == "__main__":
    main()
