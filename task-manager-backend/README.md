# Task Manager – Backend (FastAPI + SQLite/PostgreSQL)

REST API for managing tasks: create, list (with filter), view, edit, toggle complete, delete.

## Tech
Python 3.10+, FastAPI, SQLAlchemy 2.0, Pydantic v2, SQLite (default) or PostgreSQL.

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs for Swagger UI.

Tables are created automatically on startup. To run the SQL files manually:
`python init_db.py --seed`

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/tasks` | Create task |
| GET | `/tasks?status=all\|completed\|pending&skip=0&limit=100` | List / filter |
| GET | `/tasks/{id}` | Get one |
| PUT | `/tasks/{id}` | Edit (partial allowed) |
| PATCH | `/tasks/{id}/toggle` | Mark completed / pending |
| DELETE | `/tasks/{id}` | Delete |

## Error handling
- 404 – task not found
- 422 – validation failure (empty title, bad filter value)
- 500 – database error (logged, safe message returned)

## Tests
```bash
pytest -v
```

## Structure
```
app/
  main.py        # app, CORS, error handlers
  database.py    # engine, session, get_db
  models.py      # tables
  schemas.py     # request/response validation
  crud.py        # DB logic
  routers/tasks.py
sql/             # schema.sql, schema_postgres.sql, seed.sql
tests/
```
