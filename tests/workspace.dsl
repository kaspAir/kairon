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

                decisionService = container "Decision Service" {
                    description "Verwaltet Entscheidungen, Entscheidungsstatus, Entscheidungsgrundlagen und Decision Records"
                    technology "Domain Service"
                    tags "DecisionCore"
                }

                assumptionService = container "Assumption Service" {
                    description "Verwaltet Annahmensets, Parameter, Erfahrungswerte, Confidence und Gültigkeit"
                    technology "Domain Service"
                    tags "DecisionCore"
                }

                impactService = container "Impact Assessment Service" {
                    description "Bewertet Auswirkungen auf Kosten, FTE, Durchlaufzeit, Engpässe und Qualität"
                    technology "Domain Service"
                    tags "DecisionCore"
                }

                riskService = container "Risk Assessment Service" {
                    description "Bewertet Risiken, Unsicherheiten und Nebenwirkungen einer Variante"
                    technology "Domain Service"
                    tags "DecisionCore"
                }

                recommendationService = container "Recommendation Service" {
                    description "Erzeugt strukturierte Handlungsoptionen, ohne automatisch zu entscheiden"
                    technology "Domain Service"
                    tags "DecisionCore"
                }

                decisionLifecycleService = container "Decision Lifecycle Service" {
                    description "Verwaltet Zustände, Übergänge und Historie von Entscheidungen"
                    technology "Domain Service"
                    tags "DecisionLifecycle"
                }

                approvalService = container "Approval Service" {
                    description "Verwaltet Freigaben, Genehmigungen und Eskalationen"
                    technology "Domain Service"
                    tags "DecisionLifecycle"
                }

                observationService = container "Observation Service" {
                    description "Überwacht reale Auswirkungen nach der Umsetzung"
                    technology "Domain Service"
                    tags "DecisionLifecycle"
                }

                reassessmentService = container "Reassessment Service" {
                    description "Bewertet Entscheidungen nach neuen Erkenntnissen erneut"
                    technology "Domain Service"
                    tags "DecisionLifecycle"
                }

                auditTrailService = container "Audit Trail Service" {
                    description "Speichert zeitliche Lineage und Nachvollziehbarkeit"
                    technology "Domain Service"
                    tags "DecisionLifecycle"
                }

                decisionObject = container "Decision" {
                    description "Governancefähiges Entscheidungsobjekt mit Kontext, Status, Version und Verantwortlichkeit"
                    technology "Core Business Object"
                    tags "DecisionObject"
                }

                decisionVariantObject = container "Decision Variant" {
                    description "Alternative Handlungsoption innerhalb einer Entscheidung"
                    technology "Core Business Object"
                    tags "DecisionObject"
                }

                assumptionSetObject = container "Assumption Set" {
                    description "Versionierte Sammlung von Annahmen, Parametern und Erfahrungswerten"
                    technology "Core Business Object"
                    tags "DecisionObject"
                }

                scenarioVariantObject = container "Scenario Variant" {
                    description "Bewertbare Szenarioausprägung wie Best Case, Expected Case oder Worst Case"
                    technology "Core Business Object"
                    tags "DecisionObject"
                }

                simulationRunObject = container "Simulation Run" {
                    description "Reproduzierbare Ausführung einer Simulation mit referenzierten Annahmen und Szenario"
                    technology "Immutable Business Object"
                    tags "ImmutableObject"
                }

                simulationResultObject = container "Simulation Result" {
                    description "Unveränderliches Ergebnis eines Simulationslaufs"
                    technology "Immutable Business Object"
                    tags "ImmutableObject"
                }

                impactAssessmentObject = container "Impact Assessment" {
                    description "Bewertung von Auswirkungen auf Kosten, FTE, Durchlaufzeit, Qualität und Engpässe"
                    technology "Versioned Business Object"
                    tags "DecisionObject"
                }

                riskAssessmentObject = container "Risk Assessment" {
                    description "Bewertung von Risiken, Unsicherheiten, Nebenwirkungen und Confidence"
                    technology "Versioned Business Object"
                    tags "DecisionObject"
                }

                approvalRecordObject = container "Approval Record" {
                    description "Unveränderlicher Nachweis einer Freigabeentscheidung"
                    technology "Immutable Business Object"
                    tags "ImmutableObject"
                }

                observationRecordObject = container "Observation Record" {
                    description "Unveränderliche Beobachtung realer Auswirkungen nach Umsetzung"
                    technology "Immutable Business Object"
                    tags "ImmutableObject"
                }

                decisionRecordObject = container "Decision Record" {
                    description "Auditierbare Dokumentation der getroffenen Entscheidung inklusive Grundlagen"
                    technology "Immutable Business Object"
                    tags "ImmutableObject"
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

            decisionObject -> decisionVariantObject "Enthält Varianten"
            decisionObject -> assumptionSetObject "Basiert auf Annahmen"
            decisionObject -> scenarioVariantObject "Vergleicht Szenarien"
            decisionObject -> impactAssessmentObject "Nutzt Wirkungsbewertung"
            decisionObject -> riskAssessmentObject "Nutzt Risikobewertung"
            decisionObject -> approvalRecordObject "Wird freigegeben durch"
            decisionObject -> decisionRecordObject "Wird dokumentiert als"

            decisionVariantObject -> scenarioVariantObject "Kann Szenario ausprägen"
            scenarioVariantObject -> simulationRunObject "Wird simuliert durch"
            simulationRunObject -> simulationResultObject "Erzeugt Ergebnis"

            simulationResultObject -> impactAssessmentObject "Liefert Grundlage für"
            riskAssessmentObject -> approvalRecordObject "Beeinflusst Freigabe"
            impactAssessmentObject -> approvalRecordObject "Beeinflusst Freigabe"

            approvalRecordObject -> decisionRecordObject "Wird Teil von"
            observationRecordObject -> decisionRecordObject "Ergänzt Entscheidungshistorie"
            observationRecordObject -> riskAssessmentObject "Kann Neubewertung auslösen"
            observationRecordObject -> impactAssessmentObject "Vergleicht erwartete mit realer Wirkung"
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
        decisionService -> scenarioDomain "Vergleicht Entscheidungsoptionen"
        decisionService -> assumptionService "Nutzt Annahmensets"
        decisionService -> impactService "Nutzt Wirkungsbewertungen"
        decisionService -> riskService "Nutzt Risikobewertungen"
        decisionService -> recommendationService "Berücksichtigt Empfehlungen"
        decisionService -> governanceEngine "Fordert Freigaben an"

        assumptionService -> scenarioDomain "Liefert Annahmen für Szenarien"
        impactService -> simulationEngine "Bewertet Simulationsergebnisse"
        impactService -> metricsDomain "Nutzt Kennzahlen"
        riskService -> constraintDomain "Berücksichtigt Constraint-Verletzungen"
        recommendationService -> aiAdvisory "Nutzt KI-Zweitmeinung"
        recommendationService -> decisionService "Liefert Handlungsoptionen"

        governanceEngine -> decisionService "Überwacht Entscheidungsstatus"

        decisionLifecycleService -> decisionService "Verwaltet Entscheidungszustände"
        decisionLifecycleService -> approvalService "Fordert Freigaben an"
        decisionLifecycleService -> observationService "Startet Beobachtungsphase"
        decisionLifecycleService -> reassessmentService "Startet Neubewertung"
        decisionLifecycleService -> auditTrailService "Schreibt Historie"

        approvalService -> governanceEngine "Validiert Governance-Regeln"

        observationService -> metricsDomain "Überwacht KPIs"
        observationService -> impactService "Vergleicht reale Auswirkungen"

        reassessmentService -> scenarioDomain "Bewertet neue Szenarien"
        reassessmentService -> assumptionService "Berücksichtigt neue Annahmen"
        reassessmentService -> riskService "Bewertet neue Risiken"

        auditTrailService -> governanceEngine "Liefert Auditdaten"
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

        container kairon "DecisionIntelligenceCore" {
            include decisionService
            include assumptionService
            include impactService
            include riskService
            include recommendationService
            include scenarioDomain
            include simulationEngine
            include metricsDomain
            include constraintDomain
            include governanceEngine
            include aiAdvisory
            autoLayout lr
        }

        container kairon "DecisionLifecycle" {
            include decisionLifecycleService
            include decisionService
            include approvalService
            include observationService
            include reassessmentService
            include auditTrailService
            include governanceEngine
            include metricsDomain
            include impactService
            include scenarioDomain
            include assumptionService
            include riskService

            autoLayout lr
        }

        container kairon "CoreDecisionObjectModel" {
            include decisionObject
            include decisionVariantObject
            include assumptionSetObject
            include scenarioVariantObject
            include simulationRunObject
            include simulationResultObject
            include impactAssessmentObject
            include riskAssessmentObject
            include approvalRecordObject
            include observationRecordObject
            include decisionRecordObject

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

            element "DecisionCore" {
                background #ad1457
                color #ffffff
                shape roundedbox
            }

            element "DecisionLifecycle" {
                background #00695c
                color #ffffff
                shape roundedbox
            }

            element "DecisionObject" {
                background #283593
                color #ffffff
                shape roundedbox
            }

            element "ImmutableObject" {
                background #4e342e
                color #ffffff
                shape component
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