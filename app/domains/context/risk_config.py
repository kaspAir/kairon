from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


ENV_VAR_NAMES = {
    "probability_values": "KAIRON_RISK_PROBABILITY_VALUES",
    "impact_values": "KAIRON_RISK_IMPACT_VALUES",
    "severity_values": "KAIRON_RISK_SEVERITY_VALUES",
    "impact_area_values": "KAIRON_RISK_IMPACT_AREA_VALUES",
}

LEGACY_ENV_VAR_NAMES = {
    "probability_values": "KAIRON_RISK_PROBABILITY",
    "impact_values": "KAIRON_RISK_IMPACT",
    "severity_values": "KAIRON_RISK_SEVERITY",
    "impact_area_values": "KAIRON_RISK_IMPACT_AREA",
}


def _configured_values(env_name: str, defaults: tuple[str, ...]) -> tuple[str, ...]:
    raw_value = os.getenv(env_name)
    if not raw_value:
        return defaults
    values = tuple(value.strip().lower() for value in raw_value.split(",") if value.strip())
    return values or defaults


def _configured_values_with_legacy(field: str, defaults: tuple[str, ...]) -> tuple[str, ...]:
    return _configured_values(
        ENV_VAR_NAMES[field],
        _configured_values(LEGACY_ENV_VAR_NAMES[field], defaults),
    )


@dataclass(frozen=True)
class ContextTaxonomy:
    """Active structured risk taxonomy for the MVP.

    The taxonomy is configuration, not a persisted risk object. Concrete
    structured risk contexts remain owned by DecisionContextObject.

    The ``*_values`` field names are the stable public contract used by the
    context service, API responses and UI templates. The shorter properties are
    kept as UI-friendly aliases for backwards compatibility.
    """

    probability_values: tuple[str, ...] = ("low", "medium", "high")
    impact_values: tuple[str, ...] = ("low", "medium", "high")
    severity_values: tuple[str, ...] = ("low", "medium", "high", "critical")
    impact_area_values: tuple[str, ...] = (
        "cost",
        "financial",
        "operations",
        "operational",
        "compliance",
        "customer",
        "technical",
        "technology",
        "organizational",
    )

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

    @classmethod
    def from_environment(cls) -> "ContextTaxonomy":
        defaults = cls()
        return cls(
            probability_values=_configured_values_with_legacy("probability_values", defaults.probability_values),
            impact_values=_configured_values_with_legacy("impact_values", defaults.impact_values),
            severity_values=_configured_values_with_legacy("severity_values", defaults.severity_values),
            impact_area_values=_configured_values_with_legacy("impact_area_values", defaults.impact_area_values),
        )

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON/template-safe view model for the active taxonomy."""
        values = {
            "probability_values": list(self.probability_values),
            "impact_values": list(self.impact_values),
            "severity_values": list(self.severity_values),
            "impact_area_values": list(self.impact_area_values),
            "env_vars": dict(ENV_VAR_NAMES),
        }
        # Backwards-compatible aliases for older UI/API tests and templates.
        values.update({
            "probability": values["probability_values"],
            "impact": values["impact_values"],
            "severity": values["severity_values"],
            "impact_area": values["impact_area_values"],
        })
        return values


# Compatibility alias for UI code introduced before the context service import
# contract was restored. Keep ContextTaxonomy as the canonical public name.
RiskTaxonomy = ContextTaxonomy
DEFAULT_RISK_TAXONOMY = ContextTaxonomy()


def get_risk_taxonomy() -> ContextTaxonomy:
    """Return the active risk taxonomy from configuration/environment."""
    return ContextTaxonomy.from_environment()


def risk_taxonomy_view_model() -> dict[str, Any]:
    return get_risk_taxonomy().as_dict()
