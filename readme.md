# FastAPI Boilerplate

A clean FastAPI starter with async PostgreSQL (SQLAlchemy 2.x), centralized settings, structured logging, and a simple health-check endpoint.

## Features

- FastAPI app with lifespan-based startup/shutdown
- Async SQLAlchemy engine using asyncpg
- Pydantic settings-based configuration
- Basic CORS middleware setup
- Health response schema with timestamp and service status map
- Folder structure ready for routes, services, repositories, and tests

## Project Structure

```text
fastapi-recap/
	main.py
	requirements.txt
	pyproject.toml
	app/
		core/
			config.py
			logger.py
		db/
			database.py
			session.py
		models/
			db_models.py
		schemas/
			healthcheck.py
		api/
		services/
		repositories/
		tests/
```

## Requirements

- Python 3.11+
- PostgreSQL running locally or remotely

## Installation

```bash
python -m venv myvenv
```

### Windows (PowerShell)

```powershell
myvenv\Scripts\Activate.ps1
```

### Windows (Git Bash)

```bash
source myvenv/Scripts/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

The app currently reads env values from `.env` in the project root.

Create a `.env` file at the root of the repository:

```env
APP_NAME="Boilerplate fastapi"
APP_VERSION="1.0.0"
DEBUG=true
LOG_LEVEL=INFO
PORT=8000
DESCRIPTION="App description here.."

POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=Boilerplate
```

## Database Setup

This project creates tables automatically on startup using SQLAlchemy metadata.

Important: `create_all` does not create the PostgreSQL database itself. Create the database once before starting the app.

Example in `psql`:

```sql
CREATE DATABASE boilerplate;
```

Then start the app; missing tables will be created automatically.

## Run the App

Use one of the following commands from the project root.

### Development (recommended)

```bash
uvicorn main:app --reload
```

### Alternative

```bash
fastapi dev main.py
```

## API Endpoints

- `GET /` - Health check
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

Example response from `GET /`:

```json
{
	"status": "healthy",
	"timestamp": "2026-03-16T12:00:00.000000",
	"version": "1.0.0",
	"services": {}
}
```

## Notes

- If startup fails with `database does not exist`, create the database first.
- Current startup initializes DB schema at app boot.
- For production schema changes, prefer Alembic migrations over relying only on `create_all`.
