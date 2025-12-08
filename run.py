from app import create_app, db
from app.models import Article, Comment


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make objects available in the Flask shell (optional helper)."""

    return {"db": db, "Article": Article, "Comment": Comment}


if __name__ == "__main__":
    # Debug mode is fine for local development; disable for production
    app.run(debug=True)
