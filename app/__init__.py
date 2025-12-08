import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app(config_class: type[Config] = Config) -> Flask:
    """Application factory for the blog project."""

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    # Ensure the instance folder (for the SQLite DB) exists
    instance_path = os.path.join(os.path.dirname(__file__), "..", "instance")
    os.makedirs(instance_path, exist_ok=True)

    db.init_app(app)

    # Register blueprints
    from .routes import main_bp  # noqa: WPS433 (import inside function)
    from .admin_routes import admin_bp  # noqa: WPS433

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Create DB tables on first run
    with app.app_context():
        from . import models  # noqa: WPS433, F401 (ensure models are imported)

        db.create_all()

    return app
