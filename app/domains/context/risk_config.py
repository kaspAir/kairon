from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ContextTaxonomy:
    """Active structured risk taxonomy for the MVP.

    The taxonomy is configuration, not a persisted risk object. Concrete
    structured risk contexts remain owned by DecisionContextObject.

    The ``*_values`` field names are the stable public contract used by the
    context service. The shorter properties are kept as UI-friendly aliases for
    backwards compatibility with existing templates and view models.
    """

    probability_values: tuple[str, ...]
    impact_values: tuple[str, ...]
    severity_values: tuple[str, ...]
    impact_area_values: tuple[str, ...]

    @property
    def probability(self) -> tuple[str, ...]:
        return self.probability_values

    @property
    def impact(self) -> tuple[str, ...]:
        return self.impact_values

    @property
    def severity(self) -> tuple[str, ...]:
        return self.severity_values

    @property
    def impact_area(self) -> tuple[str, ...]:
        return self.impact_area_values


# Compatibility alias for UI code introduced before the context service import
# contract was restored. Keep ContextTaxonomy as the canonical public name.
RiskTaxonomy = ContextTaxonomy


def _configured_values(env_name: str, defaults: tuple[str, ...]) -> tuple[str, ...]:
    raw_value = os.getenv(env_name)
    if not raw_value:
        return defaults
    values = tuple(value.strip().lower() for value in raw_value.split(",") if value.strip())
    return values or defaults


def get_risk_taxonomy() -> ContextTaxonomy:
    """Return the active risk taxonomy from configuration/environment.

    Environment overrides are comma-separated and intentionally lightweight:
    KAIRON_RISK_PROBABILITY, KAIRON_RISK_IMPACT, KAIRON_RISK_SEVERITY,
    KAIRON_RISK_IMPACT_AREA.
    """

    return ContextTaxonomy(
        probability_values=_configured_values("KAIRON_RISK_PROBABILITY", ("low", "medium", "high")),
        impact_values=_configured_values("KAIRON_RISK_IMPACT", ("low", "medium", "high")),
        severity_values=_configured_values("KAIRON_RISK_SEVERITY", ("low", "medium", "high", "critical")),
        impact_area_values=_configured_values(
            "KAIRON_RISK_IMPACT_AREA",
            ("financial", "operational", "compliance", "technical", "organizational"),
        ),
    )


def risk_taxonomy_view_model() -> dict:
    taxonomy = get_risk_taxonomy()
    return {
        "probability": taxonomy.probability_values,
        "impact": taxonomy.impact_values,
        "severity": taxonomy.severity_values,
        "impact_area": taxonomy.impact_area_values,
    }
