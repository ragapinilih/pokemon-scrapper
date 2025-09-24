# Blueskytech Interview - Pokemon API

A simple FastAPI service with a scraper and Postgres storage. Provides endpoints to list/search Pokemon persisted from PokeAPI.

## Project Structure
- `api/` FastAPI app (`api.app:app`)
- `models/` DB access functions (`models.pokemon`)
- `database/` migration and DB pool (`database.migration`, `database.db`)
- `scrapers/` scraper runner (`scrapers.scraper`)
- `docker-compose.yml` Postgres, API, migrate, scrape

## Requirements (local dev without Docker)
- Python 3.12+
- PostgreSQL 13+

Install deps:
```bash
pip install -r requirements.txt
```

Set env (copy from sample and adjust):
```bash
cp env.sample .env
# then edit .env
```

Run migration:
```bash
python -m database.migration
```

Run API (local):
```bash
uvicorn api.app:app --reload
```

Run scraper (local):
```bash
python -m scrapers.scraper
```

## Docker & Compose
Create a `.env` from the sample in the project root:
```bash
cp env.sample .env
# edit .env as needed
```

Build and start DB + API (no migration or scraping automatically):
```bash
docker compose up --build db api
```

Run migration as a one-off job:
```bash
docker compose run --rm migrate
```

Run scraper as a one-off job:
```bash
# Uses POKEMON_SCRAPE_LIMIT from .env by default
docker compose run --rm scrape
# Override limit for a single run
POKEMON_SCRAPE_LIMIT=500 docker compose run --rm scrape
```

Stop everything:
```bash
docker compose down
```

## API
Base URL (Docker): `http://localhost:8000`

- GET `/pokemon`
  - Query params:
    - `limit` (int, 1..100, default 20)
    - `offset` (int, >=0, default 0)
    - `name` (str, optional; substring match)
  - Example:
    - `GET /pokemon?limit=20&offset=0`
    - `GET /pokemon?name=pika`
    - `GET /pokemon?pokemon_type=grass`

## Notes
- Connection pooling via `database.db` (`ThreadedConnectionPool`).
- DB schema created by `database/migration.py`.
- Scraper fetches from `https://pokeapi.co/api/v2/pokemon` and upserts rows via `models.pokemon`.

## Development Tips
- Run the API via module notation to avoid sys.path hacks:
  - `uvicorn api.app:app --reload`
- For Compose, services read environment from `.env` automatically.
- If there is issue with database using docker compose try to delete the postgres volume and re-build the db
