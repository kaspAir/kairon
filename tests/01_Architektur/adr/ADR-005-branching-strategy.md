# ADR-005 Git Branching Strategy

## Status
Accepted

## Kontext
KAIRON benötigt eine nachvollziehbare und kontrollierte Entwicklungsstrategie, um parallele Entwicklung, Qualitätssicherung und stabile Releases zu ermöglichen.

## Entscheidung
KAIRON verwendet eine Git-basierte Branching-Strategie mit:
- main
- develop
- feature/*
- hotfix/*
- release/*

## Konsequenzen
- main enthält produktionsnahe stabile Stände.
- develop dient als Integrationsbranch.
- Features werden isoliert entwickelt.
- Pull Requests dienen als Governance- und Review-Mechanismus.
- Releases können kontrolliert vorbereitet werden.
- Hotfixes können separat behandelt werden.

## Alternativen
- Trunk-based Development ohne Separation
- Direkte Entwicklung auf main
- Nicht standardisierte Branch-Nutzung

Diese Alternativen wurden verworfen, da sie Nachvollziehbarkeit und kontrollierte Qualitätssicherung erschweren würden.

## Bezug
- ADR-004 CI/CD Governance
- Architekturprinzip: Governance als Kernfähigkeit
- Structurizr Views: CI/CD Pipeline