workspace "KAIRON Architecture" "Decision-Intelligence Platform" {

    model {

        group "KAIRON" {

            enterpriseArchitect = person "Enterprise Architect" {
                description "Definiert Zielarchitektur und Governance"
            }

            simulationAnalyst = person "Simulation Analyst" {
                description "Analysiert Szenarien und Simulationen"
            }

            management = person "Management" {
                description "Bewertet organisatorische Entscheidungen"
            }

            developer = person "Developer" {
                description "Entwickelt und deployed KAIRON"
            }

            kairon = softwareSystem "KAIRON Platform" {
                description "Governance-fähige Decision-Intelligence-Plattform"

                webapp = container "Web Application" {
                    description "UI für Modellierung, Governance und Simulation"
                    technology "Flask/Jinja"
                }

                simulationEngine = container "Simulation Engine" {
                    description "Deterministische Simulationslogik"
                    technology "Python"
                }

                governanceEngine = container "Governance Engine" {
                    description "Governance, Freigaben und Auditierbarkeit"
                    technology "Python"
                }

                analyticsEngine = container "Analytics Engine" {
                    description "Kennzahlen, KPIs und Nutzenbewertungen"
                    technology "Python"
                }

                aiAdvisory = container "AI Advisory Engine" {
                    description "KI-gestützte Zweitmeinung"
                    technology "Python"
                }

                database = container "PostgreSQL Database" {
                    description "Persistente Datenhaltung"
                    technology "PostgreSQL"
                    tags "Database"
                }

                processDomain = container "Process Domain" {
                    description "Verwaltet Prozessmodelle und Prozessversionen"
                    technology "Domain Module"
                    tags "Domain"
                }

                organizationDomain = container "Organization Domain" {
                    description "Verwaltet Rollen, Organisation und Verantwortlichkeiten"
                    technology "Domain Module"
                    tags "Domain"
                }

                scenarioDomain = container "Scenario Domain" {
                    description "Verwaltet Szenarien und Varianten"
                    technology "Domain Module"
                    tags "Domain"
                }

                constraintDomain = container "Constraint Domain" {
                    description "Verwaltet Regeln und Einschränkungen"
                    technology "Domain Module"
                    tags "Domain"
                }

                decisionIntelligenceDomain = container "Decision Intelligence Domain" {
                    description "Verwaltet Bewertungen und Entscheidungsobjekte"
                    technology "Domain Module"
                    tags "Domain"
                }

                metricsDomain = container "Metrics & Analytics Domain" {
                    description "Verwaltet KPIs und Kennzahlen"
                    technology "Domain Module"
                    tags "Domain"
                }
            }

            deliveryPlatform = softwareSystem "Delivery Platform" {
                description "CI/CD- und Deployment-Plattform"

                gitRepository = container "Git Repository" {
                    description "Source Code Repository"
                    technology "Git / Bitbucket"
                }

                pipeline = container "CI/CD Pipeline" {
                    description "Build-, Test- und Deployment-Pipeline"
                    technology "Bitbucket Pipelines / GitHub Actions"
                }

                containerRegistry = container "Container Registry" {
                    description "Speichert Docker Images"
                    technology "Docker Registry"
                }

                integrationEnvironment = container "Integration Environment" {
                    description "Automatisierte Integrationsumgebung"
                    technology "Docker"
                }

                productionEnvironment = container "Production Environment" {
                    description "Produktionsumgebung"
                    technology "Swiss PaaS / On Premise"
                }
            }

            enterpriseArchitect -> kairon "Modelliert Architektur"
            simulationAnalyst -> kairon "Analysiert Szenarien"
            management -> kairon "Bewertet Auswirkungen"

            developer -> gitRepository "Entwickelt Features"
            developer -> pipeline "Startet Builds"

            gitRepository -> pipeline "Triggert Pipeline"
            pipeline -> containerRegistry "Publiziert Docker Images"
            pipeline -> integrationEnvironment "Deployt Integration"
            pipeline -> productionEnvironment "Deployt Produktion"

            integrationEnvironment -> kairon "Betreibt Integration"
            productionEnvironment -> kairon "Betreibt Produktion"

            webapp -> simulationEngine "Startet Simulationen"
            webapp -> governanceEngine "Verwaltet Governance"
            webapp -> analyticsEngine "Lädt Kennzahlen"
            webapp -> aiAdvisory "Fordert Empfehlungen an"

            simulationEngine -> database "Speichert Ergebnisse"
            governanceEngine -> database "Speichert Governance-Daten"
            analyticsEngine -> database "Liest Kennzahlen"
            aiAdvisory -> database "Analysiert Entscheidungsdaten"

            scenarioDomain -> processDomain "Referenziert Prozessvarianten"
            scenarioDomain -> organizationDomain "Referenziert Organisationsstruktur"
            scenarioDomain -> constraintDomain "Berücksichtigt Constraints"

            simulationEngine -> scenarioDomain "Verarbeitet Szenarien"
            simulationEngine -> processDomain "Nutzt Prozessmodelle"
            simulationEngine -> organizationDomain "Nutzt Organisationsdaten"
            simulationEngine -> constraintDomain "Prüft Einschränkungen"

            decisionIntelligenceDomain -> simulationEngine "Bewertet Simulationsergebnisse"
            decisionIntelligenceDomain -> metricsDomain "Nutzt Kennzahlen"
            decisionIntelligenceDomain -> scenarioDomain "Bewertet Szenarien"

            governanceEngine -> scenarioDomain "Steuert Szenariofreigaben"
            governanceEngine -> decisionIntelligenceDomain "Steuert Entscheidungsfreigaben"
            governanceEngine -> constraintDomain "Überwacht Regelkonformität"

            analyticsEngine -> metricsDomain "Verarbeitet Kennzahlen"
            aiAdvisory -> decisionIntelligenceDomain "Erzeugt Zweitmeinungen"
        }

        deploymentEnvironment "Integration" {

            deploymentNode "Integration Environment" {
                technology "Docker Host / PaaS"

                containerInstance webapp
                containerInstance simulationEngine
                containerInstance governanceEngine
                containerInstance analyticsEngine
                containerInstance aiAdvisory
                containerInstance database
            }
        }

        deploymentEnvironment "Production - Swiss PaaS" {

            deploymentNode "Swiss PaaS" {
                technology "Swiss hosted container platform"

                deploymentNode "Application Runtime" {
                    technology "Docker Runtime"

                    containerInstance webapp
                    containerInstance simulationEngine
                    containerInstance governanceEngine
                    containerInstance analyticsEngine
                    containerInstance aiAdvisory
                }

                deploymentNode "Managed Database" {
                    technology "PostgreSQL"

                    containerInstance database
                }
            }
        }

        deploymentEnvironment "Production - On Premise" {

            deploymentNode "Customer Data Center" {
                technology "On Premise Infrastructure"

                deploymentNode "Docker Host" {
                    technology "Docker Runtime"

                    containerInstance webapp
                    containerInstance simulationEngine
                    containerInstance governanceEngine
                    containerInstance analyticsEngine
                    containerInstance aiAdvisory
                }

                deploymentNode "Database Server" {
                    technology "PostgreSQL"

                    containerInstance database
                }
            }
        }
    }

    views {

        systemContext kairon "SystemContext" {
            include *
            autoLayout lr
        }

        container kairon "Containers" {
            include webapp
            include simulationEngine
            include governanceEngine
            include analyticsEngine
            include aiAdvisory
            include database
            include enterpriseArchitect
            include simulationAnalyst
            include management
            autoLayout lr
        }

        container kairon "DomainArchitecture" {
            include processDomain
            include organizationDomain
            include scenarioDomain
            include constraintDomain
            include decisionIntelligenceDomain
            include metricsDomain
            include simulationEngine
            include governanceEngine
            include analyticsEngine
            include aiAdvisory
            autoLayout lr
        }

        systemContext deliveryPlatform "DeliveryPlatform" {
            include *
            autoLayout lr
        }

        container deliveryPlatform "DeliveryPipeline" {
            include *
            autoLayout lr
        }

        deployment * "Integration" "DeploymentIntegration" {
            include *
            autoLayout lr
        }

        deployment * "Production - Swiss PaaS" "DeploymentSwissPaaS" {
            include *
            autoLayout lr
        }

        deployment * "Production - On Premise" "DeploymentOnPremise" {
            include *
            autoLayout lr
        }

        theme default

        styles {

            element "Person" {
                shape person
                background #08427b
                color #ffffff
                fontSize 22
            }

            element "Software System" {
                background #1168bd
                color #ffffff
            }

            element "Container" {
                background #438dd5
                color #ffffff
            }

            element "Database" {
                shape cylinder
                background #2e7d32
                color #ffffff
            }

            element "Domain" {
                background #6a1b9a
                color #ffffff
                shape hexagon
            }

            element "Deployment Node" {
                background #455a64
                color #ffffff
            }

            relationship "Relationship" {
                color #707070
                routing orthogonal
            }
        }
    }

    !docs docs
    !decisions docs/adr
}