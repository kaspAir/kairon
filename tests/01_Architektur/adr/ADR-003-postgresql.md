# ADR-003 PostgreSQL als produktive relationale Datenbank

## Status
Accepted

## Kontext
KAIRON benötigt eine robuste, transaktionale und produktionsfähige relationale Datenbank zur Speicherung von Entscheidungsdaten, Szenarien, Organisationen, Rollen, Kostenmodellen, Governance-Informationen und Auditdaten.

## Entscheidung
PostgreSQL wird als primäre produktive relationale Datenbank verwendet.

## Konsequenzen
- SQLAlchemy wird auf PostgreSQL ausgerichtet.
- Datenmodelle müssen PostgreSQL-kompatibel sein.
- Lokale Entwicklungsumgebungen verwenden ebenfalls PostgreSQL.
- Backup- und Restore-Strategien werden auf PostgreSQL abgestimmt.
- Spätere Erweiterungen wie Partitionierung oder Replikation bleiben möglich.

## Alternativen
- SQLite
- MySQL/MariaDB
- Cloud-spezifische Datenbankdienste

SQLite wurde nur für sehr frühe Prototypen betrachtet, jedoch wegen fehlender Produktionsfähigkeit verworfen.

## Bezug
- Architekturprinzip: Deterministischer Kern
- Architekturprinzip: Lineage by Design
- Structurizr Views: ContainerView, DeploymentIntegration