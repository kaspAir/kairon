# ADR-007: Decision Context Objects as Extensibility Layer

## Status

Accepted

## Kontext

Kairon entwickelt sich zu einer governance-fähigen Decision-Intelligence-Plattform. Der Produktkern liegt nicht in der reinen Prozessdokumentation, sondern in der nachvollziehbaren, vergleichbaren und möglichst quantifizierbaren Bewertung organisatorischer und prozessualer Entscheidungen.

Die Zielarchitektur sieht mehrere fachliche Kontextdomänen vor, darunter Organisation, Prozesse, Ressourcen, Kosten, Szenarien, Constraints, Metrics, Governance, AI Advisory sowie Organizational Dynamics & Uncertainty. Diese Domänen sind entscheidungsrelevant, simulationsrelevant und governance-relevant. Gleichzeitig sollen sie nicht zu früh als schwere, isolierte Module implementiert werden.

Insbesondere müssen zukünftige und heute noch nicht vollständig bekannte Entscheidungsfaktoren integrierbar bleiben, ohne den Decision Core grundlegend umzubauen.

## Entscheidung

Kairon führt `DecisionContextObject` als erweiterbare fachliche Abstraktion ein.

Ein Decision Context Object beschreibt eine entscheidungsrelevante Kontextinformation, die mit einer Decision verknüpft ist und später für Bewertung, Simulation, Governance, Reassessment oder Decision Records verwendet werden kann.

Beispiele für Context Types:

- process
- organization
- workforce
- risk
- assumption
- cost
- constraint
- metric
- external_factor
- human_factor
- political_factor
- implementation_risk

Das Context Object dient als Erweiterungsschicht zwischen dem stabilen Decision Core und später spezialisierten Fachdomänen wie BPMN, Organisationsmodell, HR-/Workforce-Modell, Risikomanagement, Kostenmodell oder Knowledge Graph.

## Modellierungsprinzip

Der Decision Core bleibt stabil.

Neue Entscheidungsgrundlagen werden zunächst als Context Objects modelliert. Erst wenn eine Domäne fachlich stabil, häufig genutzt und simulations- oder governancekritisch ist, wird sie zu einer spezialisierten Domäne ausgebaut.

## Vorgeschlagenes Datenmodell

Ein `DecisionContextObject` enthält mindestens:

- id
- decision_id
- context_type
- name
- description
- source
- confidence
- valid_from
- valid_to
- owner
- metadata_json
- created_at
- updated_at

## Begründung

Diese Entscheidung schützt Kairon vor zu früher Übermodellierung.

Ohne diese Abstraktion bestünde die Gefahr, dass Kairon früh zu einem Bündel isolierter Module wird:

- BPMN-Modul
- HR-Modul
- Risiko-Modul
- Organisationsmodul
- Kostenmodul

Das würde die Architektur verbreitern, bevor der Decision-Intelligence-Kern stabil genug ist.

Mit Context Objects bleibt Kairon entscheidungszentriert und zugleich erweiterbar.

## Konsequenzen

Positive Konsequenzen:

- Der Decision Core bleibt stabil.
- Neue Kontextarten können aufgenommen werden, ohne sofort neue Domänenmodelle zu erzwingen.
- Unvorhergesehene Einflussfaktoren können strukturiert erfasst werden.
- Die spätere Spezialisierung in Prozess-, Organisations-, Risiko-, Kosten- oder Graphdomänen bleibt möglich.
- Reassessment, Simulation und Governance können auf einheitliche Kontextobjekte zugreifen.
- Das Modell passt zur Zielarchitektur von Kairon, insbesondere zu Lineage, Governance und Organizational Dynamics & Uncertainty.

Negative Konsequenzen:

- `metadata_json` kann bei unsauberer Nutzung zu unstrukturierter Datenablage werden.
- Es braucht klare Regeln, wann ein Context Object in eine spezialisierte Domäne überführt wird.
- Reporting und Validierung sind zunächst weniger streng als bei vollständig spezialisierten Fachmodellen.
- Governance-Regeln für Context Types müssen schrittweise aufgebaut werden.

## Governance-Regel

Ein Context Type darf produktiv verwendet werden, wenn mindestens definiert ist:

- Zweck
- fachlicher Owner
- zulässige Datenfelder
- erwartete Datenqualität
- Relevanz für Decision, Simulation oder Governance
- Reassessment-Relevanz

## Alternativen

### Alternative 1: Jede Domäne sofort vollständig modellieren

Dies würde klare Fachmodelle ermöglichen, aber die frühe Produktentwicklung stark verlangsamen und das Risiko von Overengineering erhöhen.

Abgelehnt.

### Alternative 2: Alle Kontextinformationen nur als freie Notizen speichern

Dies wäre einfach umzusetzen, aber nicht ausreichend governancefähig, simulationsfähig oder auditierbar.

Abgelehnt.

### Alternative 3: Context Objects als flexible Erweiterungsschicht

Diese Variante verbindet frühe Flexibilität mit späterer Spezialisierbarkeit.

Angenommen.

## Bezug zur Zielarchitektur

Die Entscheidung unterstützt insbesondere folgende Architekturprinzipien:

- Entscheidungsplattform statt Dokumentation
- Konfiguration vor Programmierung
- Transparente Annahmen
- Lineage by Design
- Governance als Kernfähigkeit
- Event-ready Architecture
- Modularität
- Produktfähigkeit

Sie unterstützt außerdem die spätere Integration von:

- Organization Domain
- Process Domain
- Risk Assessment
- Assumption Sets
- Constraint Domain
- Metrics & Analytics
- Organizational Dynamics & Uncertainty
- AI Advisory

## Ergebnis

Kairon modelliert entscheidungsrelevante Kontextinformationen zunächst über Decision Context Objects.

Spezialisierte Domänen werden erst dann eingeführt, wenn fachliche Stabilität, Wiederverwendung und Governance-Relevanz ausreichend klar sind.