from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from slugify import slugify as create_slug
from werkzeug.utils import secure_filename
import os

from . import db
from .models import Article, Comment


main_bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route("/")
def index():
    """Main page with presentation text and list of recent articles."""

    articles = Article.query.order_by(Article.created_at.desc()).limit(6).all()
    return render_template("index.html", articles=articles)


@main_bp.route("/blog")
def blog():
    """Blog page with all articles and form to write new ones."""

    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template("blog.html", articles=articles)


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


@main_bp.route("/blog/write", methods=["GET", "POST"])
def write_article():
    """Public form to write and submit a new article."""

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip() or "Anonyme"
        content = request.form.get("content", "").strip()

        if not title or not content:
            return render_template(
                "write_article.html",
                error="Le titre et le contenu sont obligatoires.",
            )

        # Generate slug from title
        slug = create_slug(title)
        # Check if slug exists, if so add a number
        counter = 1
        original_slug = slug
        while Article.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to make filename unique
                import time
                timestamp = str(int(time.time()))
                name, ext = os.path.splitext(filename)
                image_filename = f"{timestamp}_{name}{ext}"
                
                # Get the Flask app's root path
                from flask import current_app
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                
                file.save(os.path.join(upload_folder, image_filename))

        article = Article(
            title=title, 
            slug=slug, 
            content=content, 
            author=author,
            image_filename=image_filename
        )
        db.session.add(article)
        db.session.commit()

        return redirect(url_for("main.article_detail", slug=article.slug))

    return render_template("write_article.html")


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