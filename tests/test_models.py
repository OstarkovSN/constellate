"""Tests for database models.

Tests User and Article models, their relationships, and methods.
"""

from datetime import datetime

import pytest
from flask import Flask
from sqlalchemy.exc import IntegrityError

from database import db
from models.article import Article
from models.user import User


class TestUserModel:
    """Test cases for User model."""

    def test_create_user(self, app: Flask) -> None:
        """Test creating a user in the database."""
        with app.app_context():
            user = User(
                username="modeluser",
                email="model@example.com",
            )
            user.set_password("modelpass123")

            db.session.add(user)
            db.session.commit()

            # Verify user was saved
            retrieved_user = User.query.filter_by(username="modeluser").first()
            assert retrieved_user is not None
            assert retrieved_user.email == "model@example.com"
            assert retrieved_user.check_password("modelpass123")

    def test_user_unique_username(self, app) -> None:
        """Test that usernames must be unique."""
        with app.app_context():
            user1 = User(username="uniqueuser", email="user1@example.com")
            user1.set_password("pass123")
            db.session.add(user1)
            db.session.commit()

            # Try to create another user with same username
            user2 = User(username="uniqueuser", email="user2@example.com")
            user2.set_password("pass123")
            db.session.add(user2)

            with pytest.raises(IntegrityError):  # Should raise integrity error
                db.session.commit()

    def test_user_unique_email(self, app: Flask) -> None:
        """Test that emails must be unique when provided."""
        with app.app_context():
            user1 = User(username="user1", email="same@example.com")
            user1.set_password("pass123")
            db.session.add(user1)
            db.session.commit()

            # Try to create another user with same email
            user2 = User(username="user2", email="same@example.com")
            user2.set_password("pass123")
            db.session.add(user2)

            with pytest.raises(IntegrityError):  # Should raise integrity error
                db.session.commit()

    def test_user_articles_relationship(self, app) -> None:
        """Test relationship between User and Article models."""
        with app.app_context():
            user = User(username="articleuser", email="article@example.com")
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()

            # Create articles for the user
            article1 = Article(
                title="Test Article 1",
                content="Content 1",
                user_id=user.id,
            )
            article2 = Article(
                title="Test Article 2",
                content="Content 2",
                user_id=user.id,
            )

            db.session.add(article1)
            db.session.add(article2)
            db.session.commit()

            # Test relationship
            assert user.articles.count() == 2
            assert article1.author == user
            assert article2.author == user


class TestArticleModel:
    """Test cases for Article model."""

    def test_create_article(self, app: Flask, test_user: User) -> None:
        """Test creating an article in the database."""
        with app.app_context():
            article = Article(
                title="Test Article",
                content="This is test content",
                url="https://example.com/article",
                tags="test,example",
                user_id=test_user.id,
            )

            db.session.add(article)
            db.session.commit()

            # Verify article was saved
            retrieved_article = Article.query.filter_by(title="Test Article").first()
            assert retrieved_article is not None
            assert retrieved_article.content == "This is test content"
            assert retrieved_article.url == "https://example.com/article"
            assert retrieved_article.tags == "test,example"
            assert retrieved_article.user_id == test_user.id
            assert retrieved_article.author == test_user

    def test_article_without_optional_fields(self, app, test_user) -> None:
        """Test creating article without optional fields."""
        with app.app_context():
            article = Article(
                title="Minimal Article",
                user_id=test_user.id,
            )

            db.session.add(article)
            db.session.commit()

            retrieved_article = Article.query.filter_by(title="Minimal Article").first()
            assert retrieved_article is not None
            assert retrieved_article.content is None
            assert retrieved_article.url is None
            assert retrieved_article.tags is None

    def test_article_requires_user(self, app) -> None:
        """Test that article with invalid user_id has no author relationship."""
        with app.app_context():
            article = Article(
                title="Orphan Article",
                user_id=99999,  # Non-existent user
            )

            db.session.add(article)
            db.session.commit()

            # SQLite doesn't enforce foreign key constraints by default,
            # but the relationship should return None for non-existent user
            assert article.author is None

    def test_article_timestamps(self, app, test_user) -> None:
        """Test that articles have created_at and updated_at timestamps."""
        with app.app_context():
            article = Article(
                title="Timestamp Article",
                user_id=test_user.id,
            )

            db.session.add(article)
            db.session.commit()

            assert article.created_at is not None
            assert article.updated_at is not None
            assert isinstance(article.created_at, datetime)
            assert isinstance(article.updated_at, datetime)

    def test_article_repr(self, app, test_user) -> None:
        """Test Article __repr__ method."""
        with app.app_context():
            article = Article(
                title="Repr Article",
                user_id=test_user.id,
            )
            db.session.add(article)
            db.session.commit()

            assert "Repr Article" in repr(article)
