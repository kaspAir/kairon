# ADR-004 CI/CD Governance als verpflichtender Delivery-Pfad

## Status
Accepted

## Kontext
KAIRON soll nachvollziehbar, reproduzierbar und qualitätsgesichert ausgeliefert werden. Fehlerhafte oder nicht getestete Änderungen dürfen nicht unkontrolliert in Integrations- oder Produktivumgebungen gelangen.

## Entscheidung
Alle Änderungen an KAIRON müssen über einen CI/CD-Pfad mit automatisierten Validierungen laufen.

## Konsequenzen
- GitHub dient als zentrale Codebasis.
- Jenkins orchestriert Builds und Tests.
- Jeder Merge muss automatisierte Smoke- und Regressionstests durchlaufen.
- Deployments erfolgen ausschließlich aus versionierten Artefakten.
- Fehlgeschlagene Tests blockieren den weiteren Delivery-Pfad.
- Pipeline-Definitionen werden versioniert.

## Alternativen
- Manuelle Deployments
- Nicht automatisierte Testprozesse
- Direkte Änderungen auf Laufzeitumgebungen

Diese Alternativen wurden verworfen, da sie Governance, Nachvollziehbarkeit und Stabilität gefährden würden.

## Bezug
- Architekturprinzip: Governance als Kernfähigkeit
- Architekturprinzip: Deterministischer Kern
- Structurizr Views: CI/CD Pipeline, Integration Runtime