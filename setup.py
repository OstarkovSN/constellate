"""Setup configuration for Constellate package.

Allows installation in development mode with: pip install -e .
"""

from setuptools import find_packages, setup

setup(
    name="constellate",
    version="0.1.0",
    description=(
        "A lightweight web app for machine learning communities to "
        "collaboratively curate and discuss research articles"
    ),
    author="OstarkovSN, Cursor",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.0",
        "flask-login>=0.6.3",
        "flask-wtf>=1.2.1",
        "sqlalchemy>=2.0.0",
        "werkzeug>=3.0.0",
        "wtforms>=3.1.0",
    ],
    python_requires=">=3.10",
)

