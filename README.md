# Constellate 🌟

## About

Constellate is a lightweight web app for machine learning communities to collaboratively curate and discuss research articles.

## Authors

OstarkovSN, Cursor ;)

## Key features

📌 Submit & Tag: Submit PDFs or arXiv links and add custom tags (e.g., "transformers," "LLMs").

🔗 Knowledge Graph: Explore papers as interconnected nodes where edges form automatically via shared tags and using LLM-created embeddings. Drag, zoom, and hover to see LLM-generated summaries.

👍 Community Curation: Vote on papers and assign presenters with one click; the graph dynamically highlights trending/assigned items.

🛠️ Full customization: Modular code for effortless tweaks, core LLM engine may be easilly changed (choose existing or create your own agent in `agents/` dir), then modify `CONSTELLATE_DEFAULT_AGENT` env variable.

## Installation

1. Install [pixi](https://pixi.sh/dev/installation/)
2. Clone the repository
3. Use pixi to install dependencies:
   ```shell
   pixi install -e prod
   ```

## Run the app

```shell
pixi run start
```

## Development

### Project Structure

```
constellate/
├── app.py                 # Main Flask application entry point
├── config.py              # Application configuration
├── database.py            # Database initialization
├── setup.py               # Package setup for pip install
├── pyproject.toml         # Project configuration (Pixi, Ruff, dependencies)
├── pytest.ini             # Pytest configuration
├── models/                # Database models
│   ├── user.py           # User SQLAlchemy model
│   └── article.py        # Article SQLAlchemy model
├── agents/                # Reserved for AI agent models (future)
├── routes/                # Flask route blueprints
│   └── auth.py           # Authentication routes (login, register, logout)
├── forms/                 # Flask-WTF form classes
│   └── auth.py           # Authentication forms
├── templates/             # Jinja2 HTML templates
│   ├── base.html         # Base template
│   └── auth/             # Authentication templates
├── tests/                 # Pytest test suite
│   ├── conftest.py       # Pytest fixtures
│   ├── test_auth.py      # Authentication tests
│   ├── test_models.py    # Model tests
│   └── test_routes.py    # Route tests
└── instance/              # Instance-specific files (created at runtime)
    └── site.db           # SQLite database
```

### Running Tests

```shell
pixi run test
```

### Linting

```shell
# Check for linting issues
pixi run lint

# Auto-format code
pixi run format
```

### Database

The SQLite database is automatically created at `instance/site.db` on first run. The database includes:

- **User model**: Authentication with username, password (hashed), and optional email
- **Article model**: Research articles with title, content, URL, tags, and author relationship

## Collaboration

Feel free to suggest your ideas by creating issues on github
