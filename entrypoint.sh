#!/usr/bin/env bash
set -euo pipefail

# Wait for Postgres
python - <<'PY'
import os, time, psycopg2
host = os.getenv('DB_HOST', 'db')
port = int(os.getenv('DB_PORT', '5432'))
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname = os.getenv('DB_NAME')
for i in range(60):
    try:
        psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname).close()
        print('Postgres is up')
        break
    except Exception as e:
        print(f'Waiting for Postgres ({e})...')
        time.sleep(1)
else:
    raise SystemExit('Postgres not available')
PY

# Start API
exec uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
