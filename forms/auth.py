"""Authentication forms for login and registration.

Defines Flask-WTF forms for user authentication.
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class LoginForm(FlaskForm):
    """Login form for user authentication.

    Fields:
        username: User's username
        password: User's password
        remember_me: Option to remember user session
        submit: Submit button
    """

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "Enter your username"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"},
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    """Registration form for new user accounts.

    Fields:
        username: Desired username
        email: Optional email address
        password: Password
        password2: Password confirmation
        submit: Submit button
    """

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "Choose a username (3-80 characters)"},
    )
    email = StringField(
        "Email (Optional)",
        validators=[Optional(), Email(), Length(max=120)],
        render_kw={"placeholder": "Enter your email (optional)"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Choose a password (min 6 characters)"},
    )
    password2 = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
        render_kw={"placeholder": "Confirm your password"},
    )
    submit = SubmitField("Register")

