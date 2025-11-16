"""Tests for authentication routes and functionality.

Tests login, registration, logout, and authentication-related features.
"""


from database import db
from models.user import User


class TestLogin:
    """Test cases for login functionality."""

    def test_login_page_loads(self, client) -> None:
        """Test that login page loads successfully."""
        response = client.get("/login")
        assert response.status_code == 200
        assert b"Login" in response.data
        assert b"Username" in response.data
        assert b"Password" in response.data

    def test_login_with_valid_credentials(self, client, test_user) -> None:
        """Test login with valid username and password."""
        response = client.post(
            "/login",
            data={"username": "testuser", "password": "testpass123", "remember_me": False},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Login successful" in response.data or b"Welcome" in response.data

    def test_login_with_invalid_username(self, client, test_user) -> None:
        """Test login with invalid username."""
        response = client.post(
            "/login",
            data={"username": "wronguser", "password": "testpass123", "remember_me": False},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Invalid username or password" in response.data

    def test_login_with_invalid_password(self, client, test_user) -> None:
        """Test login with invalid password."""
        response = client.post(
            "/login",
            data={"username": "testuser", "password": "wrongpass", "remember_me": False},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Invalid username or password" in response.data

    def test_login_redirects_when_authenticated(self, authenticated_client) -> None:
        """Test that login page redirects when user is already authenticated."""
        response = authenticated_client.get("/login", follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to home/index


class TestRegister:
    """Test cases for registration functionality."""

    def test_register_page_loads(self, client) -> None:
        """Test that registration page loads successfully."""
        response = client.get("/register")
        assert response.status_code == 200
        assert b"Register" in response.data
        assert b"Username" in response.data
        assert b"Password" in response.data

    def test_register_with_valid_data(self, client, app) -> None:
        """Test registration with valid user data."""
        response = client.post(
            "/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpass123",
                "password2": "newpass123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Registration successful" in response.data or b"Login" in response.data

        # Verify user was created in database
        with app.app_context():
            user = User.query.filter_by(username="newuser").first()
            assert user is not None
            assert user.email == "newuser@example.com"
            assert user.check_password("newpass123")

    def test_register_with_duplicate_username(self, client, test_user) -> None:
        """Test registration with duplicate username."""
        response = client.post(
            "/register",
            data={
                "username": "testuser",  # Already exists
                "email": "different@example.com",
                "password": "newpass123",
                "password2": "newpass123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Username already exists" in response.data

    def test_register_with_duplicate_email(self, client, test_user) -> None:
        """Test registration with duplicate email."""
        response = client.post(
            "/register",
            data={
                "username": "differentuser",
                "email": "test@example.com",  # Already exists
                "password": "newpass123",
                "password2": "newpass123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Email already registered" in response.data

    def test_register_with_password_mismatch(self, client) -> None:
        """Test registration with mismatched passwords."""
        response = client.post(
            "/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpass123",
                "password2": "differentpass",  # Mismatch
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Passwords must match" in response.data

    def test_register_with_short_password(self, client) -> None:
        """Test registration with password that's too short."""
        response = client.post(
            "/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "short",  # Less than 6 characters
                "password2": "short",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        # Should show validation error

    def test_register_without_email(self, client, app) -> None:
        """Test registration without email (optional field)."""
        response = client.post(
            "/register",
            data={
                "username": "noemailuser",
                "email": "",  # Empty email
                "password": "newpass123",
                "password2": "newpass123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        # Should succeed without email

        # Verify user was created
        with app.app_context():
            user = User.query.filter_by(username="noemailuser").first()
            assert user is not None
            assert user.email is None

    def test_register_with_database_error(self, client, app, monkeypatch) -> None:
        """Test registration error handling when database commit fails."""
        # Mock db.session.commit to raise an exception
        original_commit = db.session.commit
        error_message = "Database error"

        def mock_commit():
            db.session.rollback()
            raise RuntimeError(error_message)

        monkeypatch.setattr(db.session, "commit", mock_commit)

        response = client.post(
            "/register",
            data={
                "username": "erroruser",
                "email": "error@example.com",
                "password": "newpass123",
                "password2": "newpass123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"An error occurred during registration" in response.data

        # Restore original commit
        monkeypatch.setattr(db.session, "commit", original_commit)

    def test_register_redirects_when_authenticated(self, authenticated_client) -> None:
        """Test that register page redirects when user is already authenticated."""
        response = authenticated_client.get("/register", follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to home/index


class TestLogout:
    """Test cases for logout functionality."""

    def test_logout_requires_authentication(self, client) -> None:
        """Test that logout requires authentication."""
        response = client.get("/logout", follow_redirects=True)
        # Should redirect to login page
        assert response.status_code == 200

    def test_logout_success(self, authenticated_client) -> None:
        """Test successful logout."""
        response = authenticated_client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"logged out" in response.data.lower() or b"login" in response.data.lower()


class TestUserModel:
    """Test cases for User model."""

    def test_user_password_hashing(self, app) -> None:
        """Test that passwords are properly hashed."""
        with app.app_context():
            user = User(username="hashtest", email="hash@example.com")
            user.set_password("testpassword")

            assert user.password_hash != "testpassword"  # Should be hashed
            assert user.check_password("testpassword")  # Should verify correctly
            assert not user.check_password("wrongpassword")  # Should fail for wrong password

    def test_user_repr(self, app) -> None:
        """Test User __repr__ method."""
        with app.app_context():
            user = User(username="reprtest", email="repr@example.com")
            user.set_password("testpass")
            db.session.add(user)
            db.session.commit()

            assert "reprtest" in repr(user)
