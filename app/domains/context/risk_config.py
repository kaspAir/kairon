from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskTaxonomy:
    """Active structured risk taxonomy for the MVP.

    The taxonomy is configuration, not a persisted risk object. Concrete risk
    contexts remain owned by the existing Decision/Risk workflow.
    """

    probability: tuple[str, ...]
    impact: tuple[str, ...]
    severity: tuple[str, ...]
    impact_area: tuple[str, ...]


def _configured_values(env_name: str, defaults: tuple[str, ...]) -> tuple[str, ...]:
    raw_value = os.getenv(env_name)
    if not raw_value:
        return defaults
    values = tuple(value.strip().lower() for value in raw_value.split(",") if value.strip())
    return values or defaults


def get_risk_taxonomy() -> RiskTaxonomy:
    """Return the active risk taxonomy from configuration/environment.

    Environment overrides are comma-separated and intentionally lightweight:
    KAIRON_RISK_PROBABILITY, KAIRON_RISK_IMPACT, KAIRON_RISK_SEVERITY,
    KAIRON_RISK_IMPACT_AREA.
    """

    return RiskTaxonomy(
        probability=_configured_values("KAIRON_RISK_PROBABILITY", ("low", "medium", "high")),
        impact=_configured_values("KAIRON_RISK_IMPACT", ("low", "medium", "high")),
        severity=_configured_values("KAIRON_RISK_SEVERITY", ("low", "medium", "high", "critical")),
        impact_area=_configured_values(
            "KAIRON_RISK_IMPACT_AREA",
            ("financial", "operational", "compliance", "technical", "organizational"),
        ),
    )


def risk_taxonomy_view_model() -> dict:
    taxonomy = get_risk_taxonomy()
    return {
        "probability": taxonomy.probability,
        "impact": taxonomy.impact,
        "severity": taxonomy.severity,
        "impact_area": taxonomy.impact_area,
    }
