#!/bin/sh
set -eu

python - <<'PY'
import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

url = os.environ.get('DATABASE_URL')
if not url:
    raise SystemExit('DATABASE_URL is not set')

engine = create_engine(url, pool_pre_ping=True)
last_error = None
for _ in range(30):
    try:
        with engine.connect() as conn:
            conn.execute(text('select 1'))
        raise SystemExit(0)
    except OperationalError as exc:
        last_error = exc
        time.sleep(1)
raise SystemExit(f'Database not reachable: {last_error}')
PY

alembic upgrade head
exec "$@"
