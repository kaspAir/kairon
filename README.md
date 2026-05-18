# KAIRON MVP Baseline

KAIRON is a governance-capable Decision Intelligence platform. The MVP baseline provides a focused, end-to-end core for capturing decisions, comparing variants and scenarios, running deterministic simulations, documenting impact and risk, approving decisions, observing outcomes and creating an auditable Decision Record.

KAIRON is not a BPM tool and not a CRUD-only prototype. The current scope intentionally stays small so that future governance, analytics, AI advisory and enterprise modules can be added without rebuilding the workspace.

## MVP functional scope

The current MVP baseline includes:

- Decision Control Center at `/ui`
- Decision Workspace with overview, variants, scenarios, simulations, compare, risks, governance, observations and Decision Record
- Official API namespace under `/api`
- Health endpoint under `/health`
- Decision variants and scenarios
- Deterministic simulation runs
- Impact and risk assessment basics
- Approval records
- Structured, auditable Decision Record
- Observation and reassessment slice
- Decision lifecycle status transitions
- Golden Demo seed for an enterprise decision case
- Jinja-based UI using KAIRON/Sophilius branding and design tokens

Explicitly out of MVP scope:

- Neo4j
- BPMN editor
- Organigram editor
- complex IAM or multi-tenancy
- event sourcing
- CQRS
- message brokers
- Kubernetes
- React, Tailwind or another frontend framework
- AI-based decision automation

AI advisory may be prepared later, but AI must not decide.

## Repository structure

Active application assets are intentionally concentrated in the following locations:

```text
app/
  domains/              Domain models and services
  web/                  Flask/Jinja UI routes and view models
  api/                  API blueprints
  shared/               Database, logging and common infrastructure
  templates/            Active Jinja templates
  templates/components/ Reusable Jinja components
  static/css/           Active CSS, including app/static/css/kairon.css
  static/img/           Branding assets
migrations/             Alembic migration environment and versions
tests/regression/       CI regression tests
```

The following legacy/local artifacts are not part of the active baseline and should not be committed:

- root-level `test_health.py`
- `app/templates/app.zip`
- `app/templates/app/`
- `app/static/kairon.css`
- `.env` files except `.env.example`
- local SQLite databases such as `kairon.db`, `*.sqlite`, `*.sqlite3`
- `.venv`, caches and Structurizr runtime cache files

## Local development start

PowerShell on Windows:

```powershell
cd C:\Projekte\kairon
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:DATABASE_URL="sqlite:///kairon.db"
alembic upgrade head
python run.py
```

Open the UI:

```text
http://localhost:5000/ui
```

Check health:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

Check the API root:

```powershell
Invoke-RestMethod http://localhost:5000/api
```

If the local SQLite database is from an older development state, rebuild it:

```powershell
Remove-Item .\kairon.db -ErrorAction SilentlyContinue
alembic upgrade head
python run.py
```

## Golden Demo

The Golden Demo loads a complete enterprise-oriented walkthrough for:

```text
AI-based Invoice Processing Automation
```

It includes decision context, variants, scenarios, simulation results, impact data, risks, approvals, observations and a structured Decision Record.

Load it from the CLI:

```powershell
$env:DATABASE_URL="sqlite:///kairon.db"
flask --app run.py seed-demo
```

Or load it from the UI:

```text
http://localhost:5000/ui
```

Use the `Golden Demo laden` action in the Decision Control Center.

## Database migrations

KAIRON uses Alembic. The application no longer creates tables via `create_all()` during normal startup.

Apply migrations:

```bash
alembic upgrade head
```

Show the current revision:

```bash
alembic current
```

There must be exactly one Alembic head:

```bash
alembic heads
```

If multiple heads appear, create a merge revision instead of changing existing migration history.

## Regression tests

The regression test suite lives under `tests/regression`.

When running locally without Docker, start the app first in one shell:

```powershell
$env:DATABASE_URL="sqlite:///kairon.db"
alembic upgrade head
python run.py
```

Then run tests in a second shell:

```powershell
.\.venv\Scripts\Activate.ps1
pytest tests/regression
```

The Jenkins pipeline runs tests inside the containerized pipeline environment.

## Jenkins pipeline

Jenkins is expected to run as Pipeline from SCM. The Jenkinsfile should use the checked-out branch provided by Jenkins and must not perform a manual hard-coded `git clone`.

Pipeline responsibilities:

1. clean workspace
2. checkout SCM
3. build the Docker pipeline environment
4. start the database and app containers
5. run the smoke test against `/health`
6. run regression tests
7. tear down the pipeline environment

The smoke test delay/startup behavior is intentionally part of the pipeline stability contract. Do not remove it casually; it protects the build from transient startup timing issues after database initialization and migrations.

## Docker

Build and run the integration environment:

```powershell
docker compose -f docker-compose.integration.yml up --build
```

Build and run the pipeline environment:

```powershell
docker compose -f docker-compose.pipeline.yml up --build
```

The container entrypoint waits for the database, applies Alembic migrations and then starts the Flask app.

## Repository hygiene

Local runtime artifacts are excluded by `.gitignore` and `.dockerignore`.

If any local artifacts were committed previously, remove them from the Git index without deleting local files:

```bash
git rm --cached test_health.py || true
git rm --cached app/static/kairon.css || true
git rm -r --cached app/templates/app app/templates/app.zip || true
git rm -r --cached .structurizr .structurizr* || true
git rm --cached .env kairon.db *.sqlite *.sqlite3 *.db || true
git rm -r --cached .venv venv env __pycache__ .pytest_cache || true
```

Then commit the cleanup:

```bash
git add .
git commit -m "Prepare MVP baseline release"
```

## Governance baseline

All relevant MVP domain objects prepare auditability with lightweight metadata such as:

- `created_at`
- `updated_at`
- `version`
- `created_by`
- `status`

These fields intentionally remain simple. They prepare governance and traceability without introducing a workflow engine, event sourcing or complex IAM in the MVP baseline.
