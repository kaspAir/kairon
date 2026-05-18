# ADR-001 Hybrid Deployment

## Status
Accepted

## Context
KAIRON muss sowohl als Schweizer SaaS als auch On Premise betrieben werden können.

## Decision
KAIRON wird deploymentneutral und containerisiert aufgebaut.

## Consequences

- Docker als Standard
- PostgreSQL produktiv
- Keine harte Cloud-Abhängigkeit
- Austauschbare Infrastrukturservices
- Backup-/Restore-Strategie erforderlich