# KAIRON MVP Core

KAIRON ist eine governance-fähige Decision-Intelligence-Plattform. Dieser MVP-Core implementiert einen vertikalen End-to-End-Slice: Decision, Variant, Scenario, deterministische Simulation, Impact Assessment, Risk Assessment, Approval Record und Decision Record.

## Architekturstand

- Flask App Factory
- SQLAlchemy ORM
- PostgreSQL-kompatible Persistenz
- Alembic Migrationen
- Domänenorientierte Blueprints
- Service Layer statt Businesslogik in Routes
- Marshmallow Request Validation und Response Serialization
- Strukturierte JSON-Fehler
- Request Logging mit `X-Request-ID`
- Docker mit non-root User und Healthcheck

Nicht enthalten: Neo4j, KI-Entscheidungen, Kubernetes, Event Sourcing, CQRS, Message Broker, Multi-Tenancy oder komplexes IAM.

## Lokaler Start mit SQLite

```powershell
cd C:\Projekte\kairon
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DATABASE_URL="sqlite:///kairon.db"
alembic upgrade head
python run.py
```

Healthcheck:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

## API Smoke Test

```powershell
$decision = Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:5000/api/decisions" `
  -ContentType "application/json" `
  -Body (@{ title="Automatisierung Rechnungseingang"; description="OCR-Unterstützung prüfen" } | ConvertTo-Json)

$variant = Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:5000/api/decisions/$($decision.id)/variants" `
  -ContentType "application/json" `
  -Body (@{ name="Variante A"; description="Teilautomatisierung"; estimated_cost=10000; expected_benefit=25000 } | ConvertTo-Json)
```

## Docker Integration

```powershell
docker compose -f docker-compose.integration.yml up --build
```

Die App führt beim Containerstart `alembic upgrade head` aus und startet danach Flask.

## Migrationen

Neue Migration erzeugen:

```bash
alembic revision --autogenerate -m "describe change"
```

Migration anwenden:

```bash
alembic upgrade head
```

## Tests

In der Jenkins-Pipeline werden die Regressionstests im laufenden App-Container ausgeführt:

```bash
pytest tests/regression
```

## Governance-Vorbereitung

Alle relevanten Domain Objects enthalten:

- `created_at`
- `updated_at`
- `version`
- `created_by`
- `status`

Diese Felder sind bewusst leichtgewichtig gehalten. Sie bereiten Auditierbarkeit und Governance vor, ohne bereits Event Sourcing, IAM oder komplexe Freigabeworkflows einzuführen.


## Repository hygiene

Local runtime artifacts are intentionally excluded from Git: `.env`, local SQLite databases, virtual environments, Python caches, test caches and Structurizr local cache files. If any of these files were committed before this cleanup, remove them from the Git index without deleting local working files:

```bash
git rm -r --cached .structurizr .structurizr* || true
git rm --cached .env kairon.db *.sqlite *.sqlite3 *.db || true
git rm -r --cached .venv venv __pycache__ .pytest_cache || true
git add .gitignore .dockerignore Jenkinsfile
```

Jenkins is configured for Pipeline from SCM. The Jenkinsfile now uses `checkout scm`, so the build runs on the branch selected by the multibranch job or SCM configuration. There is no hard-coded `git clone -b develop` in the pipeline anymore.

## Audit actor propagation

All MVP create operations accept `created_by` in the JSON payload. If omitted, KAIRON resolves the actor from `X-Kairon-User`, then `X-User`, then defaults to `system`. This is an audit placeholder, not an IAM implementation.
