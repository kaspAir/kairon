# ADR-002 Container-first Deployment

## Status
Accepted

## Kontext
KAIRON benötigt reproduzierbare, portable und konsistente Laufzeitumgebungen für lokale Entwicklung, Integration, Test und produktive Deployments. Unterschiedliche lokale Entwicklungsumgebungen dürfen nicht zu inkonsistentem Verhalten führen.

## Entscheidung
KAIRON wird container-first entwickelt und betrieben. Anwendungen und Infrastrukturservices werden standardmäßig als Docker-Container ausgeführt.

## Konsequenzen
- Lokale Entwicklung erfolgt containerisiert.
- Integration- und Testumgebungen basieren auf Docker Compose.
- Deployments können später auf Kubernetes oder PaaS-Plattformen übertragen werden.
- Infrastrukturabhängigkeiten werden explizit versioniert.
- Reproduzierbarkeit von Laufzeitumgebungen wird erhöht.

## Alternativen
- Native lokale Installationen.
- VM-basierte Entwicklungsumgebungen.
- Nicht standardisierte Entwicklerumgebungen.

Diese Alternativen wurden verworfen, weil sie zu höherem Betriebsaufwand und inkonsistentem Verhalten führen würden.

## Bezug
- ADR-001 Hybrid Deployment
- Architekturprinzip: Produktfähigkeit
- Architekturprinzip: Konfiguration vor Programmierung
- Structurizr Views: ContainerView, DeploymentIntegration