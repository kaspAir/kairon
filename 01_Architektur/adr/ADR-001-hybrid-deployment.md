# ADR-001 Hybrid Deployment

## Status
Accepted

## Kontext
KAIRON soll als governance-fähige Decision-Intelligence-Plattform sowohl in einer Schweizer PaaS-Umgebung als auch On Premise betrieben werden können. Die Plattform darf deshalb nicht hart an einen spezifischen Cloud-Anbieter oder proprietäre Managed Services gekoppelt werden.

## Entscheidung
KAIRON wird hybrid deploymentfähig aufgebaut. Dieselbe Produktlogik muss sowohl lokal, auf einer Schweizer PaaS als auch On Premise betreibbar sein.

## Konsequenzen
- Containerisierung wird verbindlicher Architekturstandard.
- Environment-Konfiguration muss sauber getrennt sein.
- Infrastrukturservices müssen austauschbar bleiben.
- Keine harte Abhängigkeit von Cloud-spezifischen Services.
- Backup- und Restore-Fähigkeit muss früh berücksichtigt werden.
- Deployment-Modelle müssen für Integration, Schweizer PaaS und On Premise dokumentiert werden.

## Alternativen
- Reine SaaS-/Cloud-Architektur.
- Reine On-Premise-Architektur.
- Provider-spezifische Managed-Service-Architektur.

Diese Alternativen wurden verworfen, weil sie die strategische Flexibilität und spätere Kundenfähigkeit von KAIRON einschränken würden.

## Bezug
- Architekturprinzip: Produktfähigkeit
- Architekturprinzip: Konfiguration vor Programmierung
- Architekturprinzip: Governance als Kernfähigkeit
- Structurizr Views: DeploymentIntegration, DeploymentSwissPaaS, DeploymentOnPremise