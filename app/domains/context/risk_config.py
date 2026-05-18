from __future__ import annotations

import os
from dataclasses import dataclass


def _csv_or_default(env_name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw = os.getenv(env_name)
    if not raw:
        return default
    values = tuple(value.strip().lower() for value in raw.split(",") if value.strip())
    return values or default


@dataclass(frozen=True)
class ContextTaxonomy:
    """Configurable taxonomy for structured risk context values.

    The MVP ships with sensible defaults, but deployments can override the
    values via environment variables without changing code or database schema.
    Risk context objects persist the selected keys as strings in metadata_json.
    """

    probability_values: tuple[str, ...] = ("low", "medium", "high")
    impact_values: tuple[str, ...] = ("low", "medium", "high")
    severity_values: tuple[str, ...] = ("low", "medium", "high", "critical")
    impact_area_values: tuple[str, ...] = (
        "cost",
        "time",
        "quality",
        "compliance",
        "people",
        "operations",
        "reputation",
    )

    @classmethod
    def from_environment(cls) -> "ContextTaxonomy":
        defaults = cls()
        return cls(
            probability_values=_csv_or_default("KAIRON_RISK_PROBABILITY_VALUES", defaults.probability_values),
            impact_values=_csv_or_default("KAIRON_RISK_IMPACT_VALUES", defaults.impact_values),
            severity_values=_csv_or_default("KAIRON_RISK_SEVERITY_VALUES", defaults.severity_values),
            impact_area_values=_csv_or_default("KAIRON_RISK_IMPACT_AREA_VALUES", defaults.impact_area_values),
        )

    def as_dict(self) -> dict[str, tuple[str, ...]]:
        return {
            "probability": self.probability_values,
            "impact": self.impact_values,
            "severity": self.severity_values,
            "impact_area": self.impact_area_values,
        }


DEFAULT_RISK_TAXONOMY = ContextTaxonomy()


def get_risk_taxonomy() -> ContextTaxonomy:
    return ContextTaxonomy.from_environment()
