from __future__ import annotations

TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": {
        "decision_narrative.workspace.eyebrow": "Decision Narrative Workspace",
        "decision_narrative.brief.title": "Decision Brief",
        "decision_narrative.brief.empty": "Noch liegen zu wenige Informationen vor, um eine belastbare Entscheidungsgeschichte zu erzählen.",
        "decision_narrative.brief.because": "{title} wird betrachtet, weil {reason}",
        "decision_narrative.brief.options": "{count} Option(en) wurden betrachtet.",
        "decision_narrative.brief.no_options": "Es wurden noch keine Optionen dokumentiert.",
        "decision_narrative.brief.risks": "Die zentralen Risiken sind {items}.",
        "decision_narrative.brief.no_risks": "Zentrale Risiken sind noch nicht dokumentiert.",
        "decision_narrative.brief.future": "Die erwartete Zukunft wird vor allem durch {items} beschrieben.",
        "decision_narrative.brief.no_future": "Die erwartete Zukunft ist noch nicht ausreichend beschrieben.",
        "decision_narrative.brief.reassessment": "Eine spätere Überprüfung ist vorgesehen oder erforderlich.",
        "decision_narrative.brief.no_reassessment": "Ein konkreter Reassessment-Punkt ist noch nicht definiert.",
        "decision_narrative.why.title": "Warum existiert diese Entscheidung?",
        "decision_narrative.why.kicker": "Ausgangslage",
        "decision_narrative.why.empty": "Noch keine Entscheidungsbegründung dokumentiert.",
        "decision_narrative.circumstances.title": "Unter welchen Umständen wird entschieden?",
        "decision_narrative.circumstances.kicker": "Relevanter Kontext",
        "decision_narrative.circumstances.empty": "Noch keine entscheidungsrelevanten Umstände dokumentiert.",
        "decision_narrative.circumstances.processes": "Betroffene Prozesse",
        "decision_narrative.circumstances.risks": "Zentrale Risiken",
        "decision_narrative.circumstances.constraints": "Wichtige Vorgaben und Einschränkungen",
        "decision_narrative.circumstances.roles": "Verantwortliche Rollen und Einheiten",
        "decision_narrative.options.title": "Welche Optionen wurden betrachtet?",
        "decision_narrative.options.kicker": "Optionen und Szenarien",
        "decision_narrative.options.empty": "Noch keine Optionen oder Szenarien dokumentiert.",
        "decision_narrative.expected_future.title": "Welche Zukunft erwarten wir?",
        "decision_narrative.expected_future.kicker": "Zukunftsannahmen",
        "decision_narrative.expected_future.empty": "Noch keine erwartete Wirkung, Annahme oder Nutzenhypothese dokumentiert.",
        "decision_narrative.expected_future.assumptions": "Annahmen",
        "decision_narrative.expected_future.metrics": "Wirkungs- und Nutzenhinweise",
        "decision_narrative.expected_future.scenarios": "Szenarien als Zukunftsbilder",
        "decision_narrative.reassessment.title": "Was müssen wir später überprüfen?",
        "decision_narrative.reassessment.kicker": "Reassessment",
        "decision_narrative.reassessment.empty": "Noch kein Reassessment definiert.",
        "decision_narrative.reassessment.review_status": "Review-Status",
        "decision_narrative.reassessment.observations": "Beobachtete Realität",
        "decision_narrative.reassessment.open_points": "Zu überprüfende Punkte",
        "decision_narrative.first_screen.options": "Optionen",
        "decision_narrative.first_screen.risks": "Zentrale Risiken",
        "decision_narrative.first_screen.review": "Review",
        "decision_narrative.detail_disclosure.title": "Vertiefende Arbeitsbereiche",
        "decision_narrative.detail_disclosure.text": "Die folgenden Bereiche bleiben für Erfassung, Pflege und technische Vertiefung verfügbar. Die Hauptorientierung bleibt die Entscheidungsgeschichte.",
        "decision_narrative.link.compare": "Vergleich öffnen",
        "decision_narrative.link.record": "Decision Record",
        "decision_narrative.confidence": "Confidence",
        "decision_narrative.status": "Status",
        "decision_narrative.owner": "Owner",
        "decision_narrative.not_defined": "Nicht definiert",
        "decision_narrative.context.type.process": "Prozess",
        "decision_narrative.context.type.organization": "Organisation",
        "decision_narrative.context.type.workforce": "Ressource / FTE",
        "decision_narrative.context.type.risk": "Risiko",
        "decision_narrative.context.type.constraint": "Vorgabe / Constraint",
        "decision_narrative.context.type.cost": "Kosten",
        "decision_narrative.context.type.metric": "Metrik",
        "decision_narrative.context.type.assumption": "Annahme",
        "decision_narrative.context.type.external_factor": "Externer Faktor",
        "decision_workspace.title": "Decision Workspace",
        "decision_workspace.story_header": "Decision Story Header",
        "decision_workspace.why_this_decision": "Why this decision?",
        "decision_workspace.context": "Decision Context",
        "decision_workspace.expected_future": "Expected Future",
        "decision_workspace.impact": "Impact",
        "decision_workspace.reassessment": "Reassessment",
        "decision_workspace.related_objects": "Related Objects",
        "decision_workspace.related_processes": "Related Processes",
        "decision_workspace.related_risks": "Related Risks",
        "decision_workspace.related_policies": "Related Policies",
        "decision_workspace.related_scenarios": "Related Scenarios",
        "decision_workspace.related_observations": "Related Observations",
        "decision_workspace.related_governance_objects": "Related Governance Objects",
        "decision_workspace.no_related_objects": "No related objects have been documented yet.",
        "decision_workspace.no_scenarios": "No scenarios or explicit future assumptions have been documented yet.",
        "decision_workspace.no_reassessment_defined": "No reassessment has been defined yet.",
        "decision_workspace.no_decision_rationale": "No decision rationale has been documented yet.",
        "decision_workspace.influenced_by": "This decision is influenced by",
        "decision_workspace.influences": "This decision influences",
        "decision_workspace.no_influenced_by": "No influencing context has been documented yet.",
        "decision_workspace.no_influences": "No influenced objects have been documented yet.",
        "decision_workspace.status": "Status",
        "decision_workspace.created_at": "Created at",
        "decision_workspace.review_date": "Review date",
        "decision_workspace.owner": "Owner",
        "decision_workspace.confidence": "Confidence",
        "decision_workspace.governance_status": "Governance status",
        "decision_workspace.scenarios_considered": "Scenarios considered",
        "decision_workspace.expected_impact": "Expected impact",
        "decision_workspace.assumptions": "Assumptions",
        "decision_workspace.observed_reality": "Observed reality",
        "decision_workspace.review_trigger": "Review trigger",
        "decision_workspace.count_suffix": "item(s)",
        "decision_workspace.open_compare": "Open compare",
        "decision_workspace.open_decision_record": "Decision Record",
        "decision_workspace.context_help": "Relevant context objects explain the circumstances, constraints and dependencies of this decision.",
        "decision_workspace.future_help": "Scenarios, assumptions and simulations describe the future that was expected or considered.",
        "decision_workspace.reassessment_help": "Decisions remain reviewable after approval. Observations and changing assumptions can trigger reassessment.",
    },
    "en": {},
}


def translate(key: str, language: str = "de", **kwargs) -> str:
    catalog = TRANSLATIONS.get(language) or TRANSLATIONS["de"]
    template = catalog.get(key) or TRANSLATIONS["de"].get(key) or key
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template


def t(key: str, **kwargs) -> str:
    return translate(key, **kwargs)


def translation_keys(language: str = "de") -> dict[str, str]:
    catalog = TRANSLATIONS.get(language) or TRANSLATIONS["de"]
    return dict(catalog)
