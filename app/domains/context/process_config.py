from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


ENV_VAR_NAMES = {
    "levels": "KAIRON_PROCESS_LEVELS",
    "labels": "KAIRON_PROCESS_LEVEL_LABELS",
}


DEFAULT_PROCESS_LEVELS = (
    "value_stream",
    "process_domain",
    "process_group",
    "process",
    "activity",
)

DEFAULT_PROCESS_LABELS = (
    "Value Stream",
    "Process Domain",
    "Process Group",
    "Process",
    "Activity",
)


def _configured_values(env_name: str, defaults: tuple[str, ...]) -> tuple[str, ...]:
    raw_value = os.getenv(env_name)
    if not raw_value:
        return defaults
    values = tuple(value.strip() for value in raw_value.split(",") if value.strip())
    return values or defaults


@dataclass(frozen=True)
class ProcessTaxonomy:
    """Active process context taxonomy for the MVP.

    Process taxonomy is configuration. Concrete process context remains stored
    as DecisionContextObject with context_type="process".
    """

    levels: tuple[str, ...] = DEFAULT_PROCESS_LEVELS
    labels: tuple[str, ...] = DEFAULT_PROCESS_LABELS

    @classmethod
    def from_environment(cls) -> "ProcessTaxonomy":
        defaults = cls()
        levels = _configured_values(ENV_VAR_NAMES["levels"], defaults.levels)
        labels = _configured_values(ENV_VAR_NAMES["labels"], defaults.labels)
        if len(labels) != len(levels):
            labels = tuple(level.replace("_", " ").title() for level in levels)
        return cls(levels=levels, labels=labels)

    @property
    def level_options(self) -> tuple[dict[str, str], ...]:
        return tuple(
            {"value": value, "label": label}
            for value, label in zip(self.levels, self.labels, strict=False)
        )

    def label_for(self, value: str | None) -> str:
        for option in self.level_options:
            if option["value"] == value:
                return option["label"]
        return (value or "").replace("_", " ").title()

    def as_dict(self) -> dict[str, Any]:
        return {
            "levels": list(self.levels),
            "labels": list(self.labels),
            "level_options": list(self.level_options),
            "env_vars": dict(ENV_VAR_NAMES),
        }


DEFAULT_PROCESS_TAXONOMY = ProcessTaxonomy()


def get_process_taxonomy() -> ProcessTaxonomy:
    return ProcessTaxonomy.from_environment()


def process_taxonomy_view_model() -> dict[str, Any]:
    return get_process_taxonomy().as_dict()
