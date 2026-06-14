ADR-012: Decision Insight Summary Foundation

Status: Accepted

Datum: 2026-06-06

Kontext

KAIRON ist eine Decision-Intelligence-Plattform.

Der zentrale Fachgegenstand ist die Entscheidung.

Im aktuellen Architekturstand können Entscheidungen bereits mit umfangreichen Entscheidungsgrundlagen verknüpft werden:

Context Objects
Risks
Processes
Policies
Governance Objects
Scenarios
Variants
Simulations
Observations
Reassessments

Dadurch entsteht eine zunehmende Menge strukturierter Entscheidungsinformationen.

Aktuell werden diese Informationen überwiegend als einzelne Objekte, Tabellen, Listen oder Fachmodule dargestellt.

Beispiel:

Decision
├─ Risks
├─ Processes
├─ Scenarios
├─ Variants
├─ Simulations
├─ Governance
└─ Observations

Der Benutzer muss die Bedeutung dieser Informationen selbst interpretieren.

Dies führt zu einer Situation, in der KAIRON zwar Entscheidungsgrundlagen dokumentiert, aber die Entscheidung selbst noch nicht aktiv verständlich macht.

Problemstellung

Benutzer möchten nicht primär wissen:

Welche Daten wurden erfasst?

Benutzer möchten verstehen:

Was bedeuten diese Daten für die Entscheidung?

Typische Fragen sind:

Wie gut ist die Entscheidung aktuell vorbereitet?
Welche Option erscheint plausibel?
Welche Risiken sind besonders relevant?
Welche Informationen fehlen noch?
Welche Annahmen sind kritisch?
Was sollte als Nächstes getan werden?

Diese Fragen entstehen fachlich aus mehreren Domänen gleichzeitig.

Sie können nicht durch einzelne Fachmodule beantwortet werden.

Entscheidung

KAIRON führt eine neue Ebene ein:

Decision Insight Summary

Die Decision Insight Summary erzeugt aus vorhandenen Entscheidungsinformationen eine verständliche Zusammenfassung des aktuellen Entscheidungsstands.

Dabei handelt es sich zunächst um eine deterministische Interpretationsschicht.

Es werden keine KI-Modelle benötigt.

Die Summary basiert ausschließlich auf vorhandenen Daten.

Architekturprinzip

Nicht:

Data → User → Interpretation

Sondern:

Data → KAIRON → Interpretation → User

KAIRON übernimmt erstmals aktiv einen Teil der Interpretation.

Zielbild

Jede Decision soll eine automatisch erzeugte Insight Summary besitzen.

Beispiel:

Decision Summary

Diese Entscheidung untersucht zwei mögliche Vorgehensweisen.

Es wurden zwei Varianten und zwei Szenarien betrachtet.

Aktuell erscheint Variante B wirtschaftlich attraktiver.

Das zentrale Risiko betrifft die Datenqualität.

Eine Simulation wurde durchgeführt.

Für eine belastbare Entscheidung fehlen derzeit noch Beobachtungsdaten aus einem Pilotbetrieb.

Empfohlener nächster Schritt:

Pilot durchführen und Ergebnisse erfassen.
Erste Ausbaustufe

Die erste Version soll bewusst einfach bleiben.

Mögliche Bestandteile:

Decision Readiness

Beispiel:

Draft
Context Captured
Scenario Ready
Simulation Ready
Governance Ready
Reassessment Needed
Key Findings

Beispiel:

- 2 Varianten dokumentiert
- 2 Szenarien betrachtet
- 1 Risiko identifiziert
- Simulation vorhanden
- Beobachtungsdaten fehlen
Next Recommended Step

Beispiel:

Simulation durchführen

oder

Pilot-Ergebnisse erfassen

oder

Governance Review abschließen
Decision Narrative Unterstützung

Die Decision Insight Summary ergänzt die bestehende Decision Narrative.

Decision Narrative beantwortet:

Warum?
Unter welchen Umständen?
Welche Optionen?
Welche Zukunft?
Welche Überprüfung?

Decision Insight Summary beantwortet:

Was bedeutet das aktuell?

Beide Konzepte ergänzen sich.

Nicht-Ziele

Dieses ADR führt nicht ein:

automatische Entscheidungen
autonome Empfehlungen
KI-gestützte Entscheidungsfreigaben
Scoring-Magie
Black-Box-Modelle
automatisierte Governance-Freigaben

KAIRON bleibt ein Human-in-the-Loop-System.

Verantwortung verbleibt beim Menschen.

Die Summary besitzt keinen normativen Charakter. Sie beschreibt Beobachtungen und Hinweise, nicht Entscheidungen.

Governance-Prinzip

Die Summary muss erklärbar sein.

Jede Aussage muss auf vorhandene Entscheidungsinformationen zurückführbar sein.

Beispiel:

Simulation vorhanden

muss nachvollziehbar aus vorhandenen Simulationen entstehen.

Nicht aus statistischen Vermutungen.

Konsequenzen
Positive Konsequenzen

Erhöhte Verständlichkeit

Benutzer verstehen schneller, worum es bei einer Entscheidung geht.

Decision Intelligence

KAIRON entwickelt sich von Dokumentation zu Interpretation.

Bessere Navigation

Benutzer erhalten Orientierung über den aktuellen Stand.

Bessere Governance

Lücken werden sichtbar.

Wiederverwendung vorhandener Informationen

Die Summary nutzt bestehende Daten.

Keine neue Fachdomäne erforderlich.

Negative Konsequenzen

Zusätzliche Interpretationslogik muss gepflegt werden.

Regeln für Readiness und Empfehlungen müssen transparent bleiben.

Fehlende Daten können zu unvollständigen Summaries führen.

UX-Leitlinie

Die Decision Insight Summary soll niemals dominieren.

Sie soll Orientierung geben.

Nicht:

Computer says:
Choose Variant B.

Sondern:

Current findings suggest:

- Variante B hat aktuell den höheren erwarteten Nettoeffekt.
- Die Risikoannahmen sollten noch validiert werden.
- Eine Governance-Freigabe steht noch aus.

Der Benutzer bleibt Entscheider.

KAIRON bleibt Entscheidungsunterstützung.

Beziehung zur Produktvision

Dieses ADR markiert den Übergang von:

Decision Documentation

zu

Decision Intelligence

KAIRON sammelt nicht mehr nur Entscheidungsinformationen.

KAIRON beginnt, diese Informationen verständlich zusammenzuführen.

Damit entsteht die Grundlage für:

Decision Understanding
Decision Readiness
Decision Lineage
Reassessment Navigation
Organisational Learning

ohne die Verantwortung vom Menschen auf das System zu übertragen.

Die Decision Insight Summary interpretiert vorhandenes Entscheidungswissen, ersetzt jedoch weder die Decision Narrative noch die spätere Reassessment-Phase.

Architektur-Leitsatz

KAIRON soll nicht nur zeigen, welche Informationen zu einer Entscheidung existieren.

KAIRON soll helfen zu verstehen, was diese Informationen gemeinsam bedeuten.