from flask import Blueprint, jsonify, render_template, request

from . import db
from .models import Article, Comment


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Main page with presentation text and list of articles."""

    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template("index.html", articles=articles)


@main_bp.route("/article/<string:slug>")
def article_detail(slug: str):
    """Display a single article page with likes and comments."""

    article = Article.query.filter_by(slug=slug).first_or_404()
    comments = (
        Comment.query.filter_by(article_id=article.id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return render_template("article_detail.html", article=article, comments=comments)


@main_bp.route("/about")
def about():
    """Static "About us" page."""

    return render_template("about.html")


@main_bp.route("/contact")
def contact():
    """Static contact page with a simple form and contact info."""

    return render_template("contact.html")


@main_bp.route("/api/articles/<int:article_id>/like", methods=["POST"])
def api_like_article(article_id: int):
    """Increment like counter for an article and return the new value."""

    article = Article.query.get_or_404(article_id)
    article.likes = (article.likes or 0) + 1
    db.session.commit()
    return jsonify({"likes": article.likes})


@main_bp.route("/api/articles/<int:article_id>/dislike", methods=["POST"])
def api_dislike_article(article_id: int):
    """Increment dislike counter for an article and return the new value."""

    article = Article.query.get_or_404(article_id)
    article.dislikes = (article.dislikes or 0) + 1
    db.session.commit()
    return jsonify({"dislikes": article.dislikes})


@main_bp.route("/api/articles/<int:article_id>/comments", methods=["GET"])
def api_get_comments(article_id: int):
    """Return all comments for an article as JSON."""

    article = Article.query.get_or_404(article_id)
    comments = (
        Comment.query.filter_by(article_id=article.id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    data = [
        {
            "id": comment.id,
            "author_name": comment.author_name,
            "body": comment.body,
            "created_at": comment.created_at.isoformat(),
        }
        for comment in comments
    ]
    return jsonify(data)


@main_bp.route("/api/articles/<int:article_id>/comments", methods=["POST"])
def api_add_comment(article_id: int):
    """Create a new comment for an article and return it as JSON."""

    article = Article.query.get_or_404(article_id)
    data = request.get_json() or {}

    body = (data.get("body") or "").strip()
    author_name = (data.get("author_name") or "Anonymous").strip() or "Anonymous"

    if not body:
        return jsonify({"error": "Comment body is required"}), 400

    comment = Comment(article_id=article.id, author_name=author_name, body=body)
    db.session.add(comment)
    db.session.commit()

    return (
        jsonify(
            {
                "id": comment.id,
                "author_name": comment.author_name,
                "body": comment.body,
                "created_at": comment.created_at.isoformat(),
            }
        ),
        201,
    )