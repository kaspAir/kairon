workspace "KAIRON Architecture" "Decision-Intelligence Platform" {

    model {

        enterprise "KAIRON" {

            enterpriseArchitect = person "Enterprise Architect" {
                description "Definiert Zielarchitektur und Governance"
            }

            simulationAnalyst = person "Simulation Analyst" {
                description "Analysiert Szenarien und Simulationen"
            }

            management = person "Management" {
                description "Bewertet organisatorische Entscheidungen"
            }

            kairon = softwareSystem "KAIRON Platform" {
                description "Governance-faehige Decision-Intelligence-Plattform"

                webapp = container "Web Application" {
                    description "UI fuer Modellierung, Governance und Simulation"
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
                    description "KI-gestuetzte Zweitmeinung"
                    technology "Python"
                }

                database = container "PostgreSQL Database" {
                    description "Persistente Datenhaltung"
                    technology "PostgreSQL"
                    tags "Database"
                }

                processDomain = container "Process Domain" {
                    description "Verwaltet Prozessmodelle, Prozessvarianten, BPMN-Strukturen und Prozessversionen"
                    technology "Domain Module"
                    tags "Domain"
                }

                organizationDomain = container "Organization Domain" {
                    description "Verwaltet Organisationseinheiten, Rollen, Funktionen, Personen und Verantwortlichkeiten"
                    technology "Domain Module"
                    tags "Domain"
                }

                scenarioDomain = container "Scenario Domain" {
                    description "Verwaltet Basisszenarien, abgeleitete Szenarien, Varianten, Vergleichsgruppen und Versionen"
                    technology "Domain Module"
                    tags "Domain"
                }

                constraintDomain = container "Constraint Domain" {
                    description "Verwaltet Regeln, Kapazitaetsgrenzen, Budgetgrenzen und Constraint-Verletzungen"
                    technology "Domain Module"
                    tags "Domain"
                }

                decisionIntelligenceDomain = container "Decision Intelligence Domain" {
                    description "Verwaltet Impact Assessments, Benefit Cases, Risk Assessments, Recommendations und Decision Records"
                    technology "Domain Module"
                    tags "Domain"
                }

                metricsDomain = container "Metrics & Analytics Domain" {
                    description "Verwaltet Metriken, KPIs, Baselines, Targets, Benchmarks und Trends"
                    technology "Domain Module"
                    tags "Domain"
                }

                decisionContextService = container "Decision Context Service" {
                    description "Verwaltet entscheidungsbezogene Kontextobjekte als erweiterbare Grundlage fuer Simulation, Governance, Reassessment und Decision Records"
                    technology "Domain Service"
                    tags "DecisionContext"
                }

                decisionContextObject = container "DecisionContextObject" {
                    description "Generisches, entscheidungsbezogenes Kontextobjekt mit Typ, Quelle, Confidence, zeitlicher Gueltigkeit, Owner und flexiblen Metadaten"
                    technology "Core Business Object / SQLAlchemy Model"
                    tags "DecisionContextObject"
                }
            }

            enterpriseArchitect -> webapp "Modelliert Architektur"
            simulationAnalyst -> webapp "Analysiert Szenarien"
            management -> webapp "Bewertet Auswirkungen"

            webapp -> simulationEngine "Startet Simulationen"
            webapp -> governanceEngine "Verwaltet Governance"
            webapp -> analyticsEngine "Laedt Kennzahlen"
            webapp -> aiAdvisory "Fordert Empfehlungen an"
            webapp -> decisionContextService "Erfasst und zeigt entscheidungsrelevante Kontextinformationen"

            simulationEngine -> database "Speichert Ergebnisse"
            governanceEngine -> database "Speichert Governance-Daten"
            analyticsEngine -> database "Liest Kennzahlen"
            aiAdvisory -> database "Analysiert Entscheidungsdaten"
            decisionContextObject -> database "Wird persistent gespeichert"

            scenarioDomain -> processDomain "Referenziert Prozessvarianten"
            scenarioDomain -> organizationDomain "Referenziert Organisationsstruktur"
            scenarioDomain -> constraintDomain "Beruecksichtigt Constraints"

            simulationEngine -> scenarioDomain "Verarbeitet Szenarien"
            simulationEngine -> processDomain "Nutzt Prozessmodelle"
            simulationEngine -> organizationDomain "Nutzt Organisationsdaten"
            simulationEngine -> constraintDomain "Prueft Einschraenkungen"
            simulationEngine -> decisionContextService "Nutzt Kontextobjekte als Simulationsgrundlage"

            decisionIntelligenceDomain -> simulationEngine "Bewertet Simulationsergebnisse"
            decisionIntelligenceDomain -> metricsDomain "Nutzt Kennzahlen"
            decisionIntelligenceDomain -> scenarioDomain "Bewertet Szenarien"

            governanceEngine -> scenarioDomain "Steuert Szenariofreigaben"
            governanceEngine -> decisionIntelligenceDomain "Steuert Entscheidungsfreigaben"
            governanceEngine -> constraintDomain "Ueberwacht Regelkonformitaet"
            governanceEngine -> decisionContextService "Prueft Kontextobjekte fuer Governance und Freigaben"

            analyticsEngine -> metricsDomain "Verarbeitet Kennzahlen"
            analyticsEngine -> decisionContextService "Analysiert Kontextobjekte fuer Bewertungen und Reassessments"

            aiAdvisory -> decisionIntelligenceDomain "Erzeugt Zweitmeinungen"
            aiAdvisory -> decisionContextService "Nutzt Kontextobjekte fuer strukturierte Zweitmeinungen"

            decisionContextService -> decisionContextObject "Verwaltet Context Objects"
            decisionContextService -> decisionIntelligenceDomain "Verknuepft Kontextobjekte mit Decisions und Decision Records"
            decisionContextService -> processDomain "Referenziert Prozesskontext"
            decisionContextService -> organizationDomain "Referenziert Organisations- und Workforce-Kontext"
            decisionContextService -> scenarioDomain "Stellt Kontext fuer Szenarien bereit"
            decisionContextService -> constraintDomain "Beruecksichtigt Constraints und externe Faktoren"
            decisionContextService -> metricsDomain "Referenziert KPIs, Baselines und Messgroessen"
        }
    }

    views {

        systemContext kairon "SystemContext" {
            include *
            autoLayout lr
        }

        container kairon "Containers" {
            include *
            autoLayout lr
        }

        container kairon "DomainArchitecture" {
            include processDomain
            include organizationDomain
            include scenarioDomain
            include constraintDomain
            include decisionIntelligenceDomain
            include decisionContextService
            include decisionContextObject
            include metricsDomain
            include simulationEngine
            include governanceEngine
            include analyticsEngine
            include aiAdvisory
            include database
            
            autoLayout lr
        }

        container kairon "DecisionContextFramework" {

            include webapp
            include decisionContextService
            include decisionContextObject
            include decisionIntelligenceDomain
            include processDomain
            include organizationDomain
            include scenarioDomain
            include constraintDomain
            include metricsDomain
            include simulationEngine
            include governanceEngine
            include analyticsEngine
            include aiAdvisory
            include database

            autoLayout lr

            title "ADR-007 - Decision Context Objects as Extensibility Layer"

            description "Zeigt Decision Context Objects als erweiterbare Kontextschicht zwischen Decision Core und spaeter spezialisierten Kontextdomaenen."
        }

        !decision {
            date "2026-05-16"
            status "Accepted"
            title "ADR-007 Decision Context Objects as Extensibility Layer"
            content "Kairon fuehrt Decision Context Objects als Erweiterungsschicht ein, um entscheidungsrelevante Kontextinformationen flexibel, governancefaehig und spaeter spezialisierbar zu modellieren."
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

            element "DecisionContext" {
                background #00695c
                color #ffffff
                shape roundedbox
            }

            element "DecisionContextObject" {
                background #283593
                color #ffffff
                shape component
            }

            relationship "Relationship" {
                color #707070
                routing orthogonal
            }
        }
    }
}
