"""User model for authentication and user management.

Defines the User SQLAlchemy model with authentication capabilities.
"""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from database import db


class User(UserMixin, db.Model):
    """User model for authentication and user management.

    Inherits from UserMixin to provide Flask-Login functionality.

    Attributes:
        id: Primary key, unique user identifier
        username: Unique username for login
        password_hash: Hashed password (never store plain passwords)
        email: Optional email address
        created_at: Timestamp of account creation

    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # Relationship to articles (one user can have many articles)
    articles = db.relationship("Article", backref="author", lazy="dynamic")

    def set_password(self, password: str) -> None:
        """Set user password by hashing it.

        Args:
            password: Plain text password to hash and store

        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise

        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """String representation of User object."""
        return f"<User {self.username}>"

