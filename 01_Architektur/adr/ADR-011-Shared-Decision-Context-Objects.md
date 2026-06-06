ADR-00XX: Shared Decision Context Objects

Status: Accepted

Datum: 2026-06-06

Kontext

KAIRON ist eine Decision-Intelligence-Plattform.

Der zentrale Fachgegenstand ist das Decision Object.

Prozesse, Risiken, Policies, Organisationen, Annahmen, Kennzahlen, Ressourcen, Constraints und weitere Domänenobjekte dienen als Entscheidungsgrundlage.

Im aktuellen MVP werden diese Informationen überwiegend als Decision Context Objects innerhalb einer einzelnen Decision gespeichert.

Beispiel:

Decision
 ├─ Process Context
 ├─ Risk Context
 ├─ Assumption Context
 └─ Metric Context

Dieser Ansatz ermöglicht einen schnellen Einstieg und reduziert die Komplexität der ersten Produktversion.

Mit zunehmender Nutzung entstehen jedoch mehrere Herausforderungen:

dieselben Prozesse werden in mehreren Decisions erfasst
dieselben Risiken werden mehrfach dokumentiert
Policies werden dupliziert
Organisationsinformationen werden wiederholt angelegt
Zusammenhänge zwischen Decisions bleiben verborgen

Dadurch entsteht Wissensduplikation.

Zudem können wichtige Fragestellungen nicht beantwortet werden:

Welche Decisions betreffen denselben Prozess?
Welche Risiken beeinflussen mehrere Decisions?
Welche Policies erzeugen die meisten Constraints?
Welche Annahmen werden organisationsweit verwendet?
Entscheidung

Decision-relevante Fachobjekte sollen langfristig als eigenständige, wiederverwendbare Objekte modelliert werden.

Die Decision bleibt das zentrale Objekt.

Die Decision besitzt diese Fachobjekte jedoch nicht dauerhaft exklusiv, sondern referenziert sie.

Decisions referenzieren Fachobjekte. Zusätzlich wird die zum Entscheidungszeitpunkt relevante Sicht (Snapshot) auditierbar gespeichert.

Beispiel:

Process
 └─ Invoice-to-Pay

Risk
 └─ Supplier Data Quality

Policy
 └─ Procurement Policy

Decision
 ├─ references Process
 ├─ references Risk
 └─ references Policy

Context Objects bleiben als MVP-Einstieg erhalten.

Sie dienen zunächst weiterhin der schnellen Erfassung von Entscheidungsgrundlagen.

Neue Fachdomänen werden jedoch schrittweise in eigenständige Wissensobjekte überführt.

Zielbild
Decision
│
├─ references Processes
├─ references Risks
├─ references Policies
├─ references Organizations
├─ references Metrics
├─ references Constraints
├─ references Assumptions
├─ references Resources
└─ references Scenarios

Die Decision bleibt Mittelpunkt der Benutzerinteraktion.

Die Fachobjekte bilden das organisationsweite Wissensnetzwerk.

Processes erklären:
Wie die Organisation arbeitet

Risks erklären:
Welche Unsicherheiten bestehen

Policies erklären:
Welche Regeln gelten

Organizations erklären:
Wer beteiligt ist

Scenarios erklären:
Welche Zukunftsmöglichkeiten betrachtet wurden

Decisions erklären:
Welche Handlungsoption gewählt wurde und warum

Konsequenzen
Positive Konsequenzen

Wiederverwendbarkeit

Ein Prozess muss nur einmal modelliert werden.

Invoice-to-Pay
 ├─ Decision A
 ├─ Decision B
 └─ Decision C

Konsistenz

Änderungen an Fachobjekten wirken auf alle relevanten Decisions.

Traceability

Zusammenhänge zwischen Decisions werden sichtbar.

Decision Intelligence

KAIRON kann später organisationsweite Analysen durchführen.

Beispiele:

meistbetroffene Prozesse
häufigste Risiken
wiederkehrende Annahmen
Governance-Hotspots
Decision Lineage

Skalierbarkeit

Die Architektur unterstützt spätere Graph- und Wissensmodellierung ohne Änderung des Produktkerns.

Negative Konsequenzen

Höhere Modellkomplexität

Referenzen müssen verwaltet werden.

Lebenszyklen von Fachobjekten müssen definiert werden.

Versionierung wird wichtiger.

Architekturprinzip: Referenz + Version

Decision
 ├─ Process Invoice-to-Pay v3
 ├─ Risk Supplier Quality v2
 └─ Policy Procurement v5

Denn Governance ohne Versionsbezug wird später schwierig.

UX-Leitlinie

Benutzer arbeiten weiterhin mit Decisions.

Benutzer arbeiten nicht mit Knoten, Kanten oder technischen Referenzmodellen.

Die Referenzierung soll über verständliche Auswahlmechanismen erfolgen.

Beispiel:

Relevanter Prozess

[ Invoice-to-Pay ▼ ]

Nicht:

Process Reference ID

Die Wissensstruktur bleibt weitgehend unsichtbar.

KAIRON präsentiert Entscheidungen, nicht Datenmodelle.

Nicht-Ziele

Dieses ADR führt nicht ein:

Neo4j
Graphvisualisierung
Node-/Edge-UI
Relationship Explorer
technische Wissensgraphen

Diese Konzepte können später ergänzt werden.

Das Ziel dieses ADR ist ausschließlich die Wiederverwendbarkeit und Referenzierbarkeit von Entscheidungsgrundlagen.

Beziehung zur Produktvision

Dieses ADR unterstützt die langfristige Vision von KAIRON als Decision-Intelligence-Plattform.

Die Decision bleibt der Hauptdarsteller.

Prozesse, Risiken, Policies, Organisationen und weitere Domänen bleiben wichtige Grundlagen, werden jedoch als wiederverwendbares Organisationswissen modelliert.

Dadurch entsteht schrittweise ein organisationsweites Entscheidungsgedächtnis, ohne den Fokus von der Entscheidung auf technische Modellierungsstrukturen zu verlagern.