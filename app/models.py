from datetime import datetime

from . import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default="Anonyme")
    category = db.Column(db.String(50), default="Général")
    tags = db.Column(db.String(255), default="")
    image_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

    comments = db.relationship(
        "Comment",
        backref="article",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Article {self.title!r}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"), nullable=False)
    author_name = db.Column(db.String(80))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Comment {self.id} on article {self.article_id}>"
