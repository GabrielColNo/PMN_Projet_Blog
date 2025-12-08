import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration for the blog application."""

    # IMPORTANT: change this in a real deployment
    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-me-in-production"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + os.path.join(basedir, "instance", "blog.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Single admin user credentials (can be overridden by environment variables)
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME") or "admin"
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "admin123"
