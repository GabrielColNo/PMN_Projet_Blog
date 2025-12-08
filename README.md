# PMN_Projet_Blog

A school project for PMN: a small blog built with HTML5/CSS and a Python backend using Flask and SQLite.

## What was added

The repository now contains a complete, database-backed blog application with a minimal frontend:

- **Flask application factory** (`app/__init__.py`) with a configurable `Config` class (`config.py`).
- **SQLite database integration** via Flask-SQLAlchemy (`app/models.py`, `instance/blog.db`).
- **Article model** with title, slug, content, timestamps, likes and dislikes counters.
- **Comment model** linked to articles.
- **Public routes** (`app/routes.py`):
  - Home page listing all articles.
  - Article detail page with comments.
  - JSON API endpoints to like/dislike an article and to list/add comments.
- **Admin area** (`app/admin_routes.py`):
  - Password-protected login for the admin user.
  - Dashboard listing all articles.
  - Create, edit and delete articles through simple forms.
- **Frontend templates** (`app/templates/`):
  - `base.html` – shared layout (header, nav, footer, flashes).
  - `index.html` – list of articles on the home page.
  - `article_detail.html` – article page with likes/dislikes and comments.
  - `admin_login.html` – admin login form.
  - `admin_dashboard.html` – admin list of articles.
  - `admin_article_form.html` – form for creating and editing articles.
- **Static assets** (`app/static/`):
  - `style.css` – basic styling for layout, articles, forms and admin pages.
  - `js/main.js` – simple JavaScript for like/dislike buttons and posting comments via the JSON API.
- A `run.py` entrypoint to start the development server.

## Requirements

- Python 3.10+ (3.11 recommended)
- `pip` (Python package manager)

All Python dependencies are listed in `requirements.txt` (Flask, Flask-SQLAlchemy, etc.).

## How to initialize and run the project (Windows / PowerShell)

From the project root (`PMN_Projet_Blog`):

1. **Create and activate a virtual environment (recommended)**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install Python dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

3. **(Optional but recommended) Configure environment variables**

   By default, the app uses safe-but-simple defaults defined in `config.py`:

   - `SECRET_KEY`: used by Flask for sessions.
   - `DATABASE_URL`: falls back to a local SQLite file in the `instance` folder.
   - `ADMIN_USERNAME` / `ADMIN_PASSWORD`: credentials for the admin area (default `admin` / `admin123`).

   You can override them in PowerShell before starting the app, for example:

   ```powershell
   $env:SECRET_KEY = "your-secret-key-here"
   $env:ADMIN_USERNAME = "myadmin"
   $env:ADMIN_PASSWORD = "a-strong-password"
   ```

4. **Run the development server**

   ```powershell
   python run.py
   ```

   On first run, the app will automatically create the SQLite database file in the `instance` directory and create the required tables.

5. **Open the blog in your browser**

   - Public site: <http://127.0.0.1:5000/>
   - Admin area: <http://127.0.0.1:5000/admin>

   Log in to the admin area with the admin credentials (either the defaults or the ones you configured via environment variables), then create your first article from the dashboard.

## Project structure (overview)

- `run.py` – starts the Flask development server.
- `config.py` – configuration (secret key, database URL, admin credentials).
- `requirements.txt` – Python dependencies.
- `app/` – main application package:
  - `__init__.py` – application factory and database initialization.
  - `models.py` – `Article` and `Comment` models.
  - `routes.py` – public routes and JSON APIs for likes/dislikes and comments.
  - `admin_routes.py` – admin login, dashboard, and article management.
- `instance/` – holds the SQLite database file (`blog.db`) created at runtime.
