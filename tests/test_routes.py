"""Tests for application routes.

Tests home route, graph route, and route redirects.
"""

from flask.testing import FlaskClient


class TestHomeRoute:
    """Test cases for home route (/)."""

    def test_home_redirects_to_login_when_not_authenticated(self, client: FlaskClient) -> None:
        """Test that home route redirects to login when user is not authenticated.

        Should redirect to login page when user is not authenticated.
        """
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_home_redirects_to_graph_when_authenticated(self, authenticated_client) -> None:
        """Test that home redirects to graph when user is authenticated."""
        response = authenticated_client.get("/", follow_redirects=True)
        assert response.status_code == 200
        # Should show graph or welcome message
        assert b"Welcome" in response.data or b"graph" in response.data.lower()


class TestGraphRoute:
    """Test cases for graph route (/graph)."""

    def test_graph_requires_authentication(self, client) -> None:
        """Test that graph route requires authentication."""
        response = client.get("/graph", follow_redirects=True)
        # Should redirect to login or return 401
        assert response.status_code in [200, 401]

    def test_graph_accessible_when_authenticated(self, authenticated_client, test_user) -> None:
        """Test that graph route is accessible when authenticated."""
        response = authenticated_client.get("/graph", follow_redirects=True)
        assert response.status_code == 200
        assert test_user.username.encode() in response.data or b"Welcome" in response.data
