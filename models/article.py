"""Article model for research article management.

Defines the Article SQLAlchemy model for storing research articles.
"""

from database import db


class Article(db.Model):
    """Article model for storing research articles.

    Attributes:
        id: Primary key, unique article identifier
        title: Article title
        content: Article content or description
        url: URL to the article (arXiv link, PDF, etc.)
        tags: Comma-separated tags for categorization
        user_id: Foreign key to the user who submitted the article
        created_at: Timestamp of article creation
        updated_at: Timestamp of last update

    """

    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(),
                          onupdate=db.func.now())

    def __repr__(self) -> str:
        """String representation of Article object."""
        return f"<Article {self.title}>"

