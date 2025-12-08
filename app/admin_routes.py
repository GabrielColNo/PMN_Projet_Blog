from datetime import datetime
from functools import wraps

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import db
from .models import Article


admin_bp = Blueprint("admin", __name__)


def login_required(view_func):
    """Decorator to restrict access to logged-in admin only."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login", next=request.url))
        return view_func(*args, **kwargs)

    return wrapper


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """Simple admin login page using credentials from the config."""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        cfg = current_app.config

        if username == cfg.get("ADMIN_USERNAME") and password == cfg.get("ADMIN_PASSWORD"):
            session["admin_logged_in"] = True
            flash("Logged in as admin.", "success")
            next_url = request.args.get("next") or url_for("admin.dashboard")
            return redirect(next_url)

        flash("Invalid credentials.", "danger")

    return render_template("admin_login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    """Log the admin out and clear the session flag."""

    session.pop("admin_logged_in", None)
    flash("Logged out.", "info")
    return redirect(url_for("main.index"))


@admin_bp.route("/")
@login_required
def dashboard():
    """Admin dashboard listing all articles."""

    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template("admin_dashboard.html", articles=articles)


@admin_bp.route("/articles/new", methods=["GET", "POST"])
@login_required
def create_article():
    """Create a new article (page creation tool)."""

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        slug = (request.form.get("slug") or "").strip()
        content = (request.form.get("content") or "").strip()

        if not title or not slug or not content:
            flash("Title, slug, and content are required.", "danger")
            return render_template("admin_article_form.html", action="create")

        if Article.query.filter_by(slug=slug).first():
            flash("Slug already exists; choose another one.", "danger")
            return render_template("admin_article_form.html", action="create")

        article = Article(title=title, slug=slug, content=content)
        db.session.add(article)
        db.session.commit()

        flash("Article created.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin_article_form.html", action="create")


@admin_bp.route("/articles/<int:article_id>/edit", methods=["GET", "POST"])
@login_required
def edit_article(article_id: int):
    """Edit an existing article."""

    article = Article.query.get_or_404(article_id)

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        slug = (request.form.get("slug") or "").strip()
        content = (request.form.get("content") or "").strip()

        if not title or not slug or not content:
            flash("Title, slug, and content are required.", "danger")
            return render_template(
                "admin_article_form.html",
                action="edit",
                article=article,
            )

        existing = Article.query.filter_by(slug=slug).first()
        if existing and existing.id != article.id:
            flash("Slug already exists; choose another one.", "danger")
            return render_template(
                "admin_article_form.html",
                action="edit",
                article=article,
            )

        article.title = title
        article.slug = slug
        article.content = content
        article.updated_at = datetime.utcnow()
        db.session.commit()

        flash("Article updated.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin_article_form.html", action="edit", article=article)


@admin_bp.route("/articles/<int:article_id>/delete", methods=["POST"])
@login_required
def delete_article(article_id: int):
    """Delete an article."""

    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()

    flash("Article deleted.", "info")
    return redirect(url_for("admin.dashboard"))
