ADR-010 — External Integration and Context Import Architecture
Status

Accepted

Kontext

Unternehmen besitzen bereits:

Prozessmanagement-Systeme
GRC-Systeme
Risikomanagement-Systeme
ERP-Systeme
EA-Tools
HR-Systeme
Dokumentenmanagement-Systeme

KAIRON darf keine Doppelerfassung erzwingen.

Entscheidung

KAIRON stellt standardisierte Import- und Integrationsschnittstellen bereit.

Architekturprinzipien
1. REST/JSON ist Standard

Primäre Integrationsform:

REST
JSON
OpenAPI
2. SOAP bleibt optional möglich

Nur für Legacy-/Enterprise-Umgebungen.

Nicht Bestandteil des MVP.

3. Importierte Objekte bleiben fachliche Kontextobjekte

Beispiel:

Prozess aus Signavio
Risiko aus Archer
Organisation aus SAP

werden in KAIRON als Context Objects eingebunden.

4. Kairon wird nicht System of Record

Das Quellsystem bleibt führend.

KAIRON wird:

Decision Intelligence Layer
Governance Layer
Reasoning Layer
5. Herkunft bleibt nachvollziehbar

Jedes importierte Objekt besitzt:

source_system
external_id
import_timestamp
last_sync
confidence
6. Beziehungen werden in Kairon modelliert

Beispiel:

Prozess
↔ Risiko
↔ Organisation
↔ Entscheidung
↔ Szenario

Diese Verknüpfungen entstehen in KAIRON.

MVP

Nicht bauen:

ESB
Event Bus
Kafka
komplexe Synchronisation

Vorbereiten:

Source Metadata
Import-Konzept
REST Foundation