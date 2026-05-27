ADR-008 — Identity, Responsibility and Scope Model
Status

Accepted

Kontext

KAIRON entwickelt sich von einer reinen Entscheidungs- und Governance-Anwendung zu einer governancefähigen Decision-Intelligence-Plattform.

Dabei reicht ein klassisches rollenbasiertes Berechtigungsmodell nicht aus.

KAIRON muss nachvollziehbar modellieren können:

wer Entscheidungen treffen darf
wer Entscheidungsgrundlagen modellieren darf
wer Risiken, Prozesse, Szenarien oder Kontexte verantwortet
innerhalb welchen organisatorischen oder fachlichen Bereichs gehandelt werden darf
welche Governance-Wirkung eine Handlung entfalten darf
warum eine Person legitimiert war, eine bestimmte Handlung vorzunehmen
wie Verantwortlichkeiten delegiert wurden
wie Sichtbarkeit und Zuständigkeit zusammenhängen

Zusätzlich soll KAIRON später:

konfigurierbare Organisations- und Prozesshierarchien unterstützen
verschiedene Governance-Strukturen abbilden können
unterschiedliche Fachsprachen und Taxonomien erlauben
auditierbar bleiben
Public-Decision- und Enterprise-Governance unterstützen

Ein simples Modell wie:

Admin
Editor
Viewer

ist dafür nicht ausreichend.

Entscheidung

KAIRON verwendet kein rein rollenbasiertes Berechtigungsmodell.

Stattdessen verwendet KAIRON ein:

Scope-basiertes Identity & Responsibility Model

Berechtigungen entstehen nicht allein durch Rollen.

Berechtigungen entstehen durch die Kombination aus:

Principal
+ Role
+ Capability
+ Scope
+ Governance Level
+ Validity
Architekturprinzipien
1. Verantwortlichkeit statt bloßer Berechtigung

KAIRON modelliert nicht nur technische Zugriffe.

KAIRON modelliert legitimierte Verantwortlichkeit innerhalb organisatorischer und fachlicher Räume.

Eine Person darf etwas nicht einfach „weil sie Admin ist“, sondern weil:

sie eine fachliche Rolle besitzt
innerhalb eines bestimmten Scopes handelt
eine bestimmte Capability besitzt
eine bestimmte Governance-Wirkung entfalten darf
das Assignment gültig ist
die Handlung auditierbar bleibt
2. Scope ist zentral

Scope ist ein eigenständiges Governance-Objekt.

Eine Rolle gilt niemals automatisch global.

Beispiele:

nur bestimmte Business Unit
nur bestimmte Prozessdomäne
nur bestimmte Risikokategorie
nur bestimmte Geography
nur bestimmte Szenariotypen
nur bestimmte Governance-Level
nur bestimmte Entscheidungsräume

Scope bestimmt:

Sichtbarkeit
Modellierungsrechte
Governance-Rechte
Delegationsmöglichkeiten
Verantwortungsräume
3. Fachliche Verantwortung und technische Capability werden getrennt

Eine Rolle beschreibt fachliche Verantwortung.

Eine Capability beschreibt technische Handlungsfähigkeit.

Beispiel:

Role:
Process Specialist

Capability:
process.model.edit

Scope:
Finance → Core Processes → Invoice-to-Pay

Dadurch bleibt das Modell flexibel und governancefähig.

Scopes können hierarchisch verschachtelt sein.

4. Governance Level ist eigenständige Dimension

KAIRON unterscheidet zwischen:

sehen
kommentieren
modellieren
validieren
reviewen
freigeben
überschreiben
auditieren

Governance-Wirkung wird explizit modelliert.

5. Assignments sind auditierbar und zeitlich gültig

Assignments verbinden:

Principal
Role
Capability
Scope
Governance Level
Validity

Assignments müssen nachvollziehbar bleiben:

wer sie erstellt hat
wann sie gültig waren
warum sie vergeben wurden
wann sie geändert wurden
ob sie delegiert wurden
6. Delegation ist ein Governance-Objekt

Delegation wird explizit modelliert.

Beispiele:

Decision Owner delegiert Analyse
Governance Board delegiert Review
Process Owner delegiert Modellierung

Delegation muss auditierbar bleiben.

7. Sichtbarkeit ist Teil der Governance

Visibility Rules sind keine reine UI-Funktion.

Sie sind Teil der Governance-Architektur.

Beispiele:

Ein Auditor sieht nur freigegebene Records.
Ein Specialist sieht nur seinen Scope.
Ein Governance Committee sieht nur High-Impact-Decisions.
8. Fachliche Hierarchien sind taxonomy-driven

KAIRON modelliert fachliche Hierarchien nicht hartcodiert.

Beispiele:

Eine Organisation verwendet:

Value Stream
→ Process Domain
→ Process Group
→ Process

Eine andere Organisation verwendet:

Capability
→ Domain
→ Service
→ Activity

KAIRON unterstützt konfigurierbare Hierarchy Taxonomies.

9. BPMN ist nicht die Kernlogik

KAIRON startet nicht als BPMN-zentrierte Plattform.

Zuerst modelliert KAIRON:

Verantwortlichkeiten
Entscheidungsräume
Kontextobjekte
Risiken
Constraints
Governance
Entscheidungsrouten
fachliche Hierarchien

BPMN kann später ergänzt werden:

Darstellung
Import/Export
Spezialmodellierung

aber nicht als dominierende Kernarchitektur.

10. Decision Spaces sind eigenständige organisatorische Räume

KAIRON unterscheidet organisatorische Entscheidungsräume.

Beispiele:

Enterprise Transformation
Procurement Governance
HR Governance
Public Policy
Critical Infrastructure

Decision Spaces beeinflussen:

Sichtbarkeit
Zuständigkeit
Governance
Delegation
Verantwortlichkeit
11. Trennung zwischen Knowledge Contributors und Decision Actors

KAIRON unterscheidet zwischen:

Knowledge Contributors

Personen, die Entscheidungsgrundlagen modellieren:

Process Specialists
Risk Specialists
Scenario Analysts
Organization Architects
Decision Actors

Personen, die Entscheidungen treffen oder freigeben:

Decision Owners
Governance Boards
Approvers
Review Committees

Diese Trennung ist zentral für Governance, Auditability und Legitimation.

Konsequenzen
Positive Konsequenzen
hohe Governancefähigkeit
nachvollziehbare Verantwortlichkeiten
flexible Organisationsmodellierung
konfigurierbare Fachhierarchien
gute Erweiterbarkeit
geeignet für Enterprise- und Public-Governance-Kontexte
saubere Trennung zwischen Verantwortung und Berechtigung
bessere Auditability
spätere Unterstützung komplexer Governance-Modelle möglich
Negative Konsequenzen
höhere konzeptionelle Komplexität
mehr Modellierungsaufwand
anspruchsvollere Rechteauflösung
spätere Scope-Auswertung potenziell komplex
Delegationslogik benötigt saubere Governance-Regeln
Gefahr von Overengineering
MVP-Entscheidung

Für den MVP wird bewusst keine vollständige IAM-/Policy-Engine gebaut.

Der MVP verwendet vereinfachte Rollen:

Decision Owner
Contributor
Specialist
Reviewer
Approver
Observer
Admin

Die Architektur wird jedoch bereits so vorbereitet, dass:

Capabilities
Scopes
Governance Levels
Assignments
Delegation
Visibility Rules

später ergänzt werden können.

Nicht-Ziele für den MVP

Nicht Bestandteil des MVP:

vollständige Mandantenfähigkeit
komplexes IAM
externe Identity Provider
SSO
Policy DSL
Graph-basierte Rechteauflösung
vollständige BPMN-Suite
komplexe Delegations-Engine
vollständige Legitimacy-Engine
Beziehung zur Zielarchitektur

Dieses ADR unterstützt insbesondere:

Operational Decision Loop
Governance Architecture
Decision Traceability
Legitimacy Trace
Public Decision Governance
Structured Context Objects
konfigurierbare Taxonomies
spätere Graph-/Knowledge-Modelle
Langfristige Perspektive

Langfristig soll KAIRON nicht nur modellieren:

Wer durfte etwas tun?

sondern:

Warum durfte diese Person
innerhalb dieses organisatorischen Kontextes
diese Handlung mit dieser Wirkung durchführen?

Damit wird Verantwortlichkeit selbst Teil der Governance-Architektur.

KAIRON modelliert nicht nur Handlung,
sondern legitimierte Handlung innerhalb eines nachvollziehbaren organisatorischen Kontextes.