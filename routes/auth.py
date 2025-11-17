"""Authentication routes for user login and registration.

Handles user authentication, login, and registration functionality.
"""

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from database import db
from forms.auth import LoginForm, RegisterForm
from models.user import User

# Create blueprint for authentication routes
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    """User login route.

    GET: Display login form
    POST: Process login form submission

    Returns:
        Response: Rendered login template or redirect to home

    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        # Query user by username
        user = User.query.filter_by(username=form.username.data).first()

        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            # Redirect to next page or home
            next_page = request.args.get("next")
            if not next_page or not next_page.startswith("/"):
                next_page = url_for("index")

            flash("Login successful!", "success")
            return redirect(next_page)
        flash("Invalid username or password.", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> Response | str:
    """User registration route.

    GET: Display registration form
    POST: Process registration form submission

    Returns:
        Response: Rendered registration template or redirect to login

    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()

    if form.validate_on_submit():
        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists. Please choose a different one.", "error")
            return render_template("auth/register.html", form=form)

        # Check if email already exists (if provided)
        if form.email.data and User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please use a different email.", "error")
            return render_template("auth/register.html", form=form)

        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data if form.email.data else None,
        )
        user.set_password(form.password.data)

        # Add user to database
        try:
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception:
            db.session.rollback()
            flash("An error occurred during registration. Please try again.", "error")

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout() -> Response:
    """User logout route.

    Requires authentication. Logs out the current user and redirects to login.

    Returns:
        Response: Redirect to login page

    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

