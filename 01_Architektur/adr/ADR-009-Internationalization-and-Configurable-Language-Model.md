ADR-009 — Internationalization and Configurable Language Architecture
Status

Accepted

Kontext

KAIRON soll in unterschiedlichen Organisationen, Branchen, Ländern und Verwaltungskontexten eingesetzt werden können.

Dabei unterscheiden sich:

Sprache
Fachbegriffe
Prozessbezeichnungen
Governance-Begriffe
Rollen
Organisationsstrukturen
Taxonomien

Eine hart codierte Sprache oder feste Begriffswelt widerspricht der Zielarchitektur.

Entscheidung

KAIRON verwendet ein konfigurierbares Internationalisierungsmodell.

Es werden unterschieden:

technische Schlüssel
sprachabhängige Labels
organisationsabhängige Fachbegriffe
Architekturprinzipien
1. Technische Schlüssel bleiben stabil

Beispiel:

process
risk
decision
scenario
value_stream

Diese Schlüssel ändern sich nie.

2. Labels sind sprachabhängig

Beispiel:

process

de: Prozess
en: Process
fr: Processus
it: Processo
3. Taxonomien sind ebenfalls übersetzbar

Beispiel:

value_stream

de: Wertstrom
en: Value Stream
4. Organisationen können Begriffe überschreiben

Beispiel:

value_stream

Organisation A:
Value Stream

Organisation B:
Capability Stream

Organisation C:
Business Flow
MVP

Für den MVP:

Flatfile-basiert
YAML oder JSON
keine DB-Migration

Später optional:

Datenbank
UI-Verwaltung
Versionierung
Konsequenzen

Positiv:

mehrsprachig
konfigurierbar
international einsetzbar
Public-Sector-fähig

Negativ:

höhere Komplexität
konsequente Verwendung von Translation Keys erforderlich