# KAIRON

KAIRON ist eine governance-fähige Decision-Intelligence-Plattform zur Modellierung, Simulation und Bewertung organisatorischer Entscheidungen.

## Zielsetzung

KAIRON unterstützt Unternehmen bei:

- Entscheidungsfindung
- Szenarioanalyse
- Governance
- Simulation organisatorischer Auswirkungen
- KPI- und Nutzenbewertung
- Auditierbarkeit und Lineage

## Architekturprinzipien

- Deterministischer Kern
- Governance by Design
- Lineage by Design
- Konfiguration vor Programmierung
- KI nur beratend

## Architektur

Die Architektur wird modellgetrieben entwickelt:

- Structurizr DSL
- C4 Model
- Domain-driven Architecture
- Hybrid Deployment
- Container-first

## Technologie-Stack

- Python
- Flask
- PostgreSQL
- Docker
- Jenkins
- GitHub

## Deployment

Lokale Integrationsumgebung:

```bash
docker compose -f docker-compose.integration.yml up --build -d



```powershell id="ms4y1l"
git add .
git commit -m "Add README and project documentation"
git push

Branching Strategy
main
→ produktionsfähiger Stand

develop
→ Integrationsbranch

feature/*
→ neue Features

hotfix/*
→ produktionsnahe Korrekturen

release/*
→ optionale Release-Stabilisierung später