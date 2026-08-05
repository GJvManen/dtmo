from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from .base import Connector


@dataclass(frozen=True)
class ConnectorDefinition:
    connector_id: str
    title: str
    source_type: str
    reliability: str
    schedule_minutes: int
    enabled_by_default: bool
    factory: Callable[[], Connector]


class ConnectorCatalog:
    def __init__(self) -> None:
        self._definitions: dict[str, ConnectorDefinition] = {}

    def register(self, definition: ConnectorDefinition) -> None:
        if definition.connector_id in self._definitions:
            raise ValueError(f"duplicate connector: {definition.connector_id}")
        if definition.reliability not in {"authoritative", "primary", "trusted", "community"}:
            raise ValueError("invalid reliability")
        if definition.schedule_minutes < 5:
            raise ValueError("connector interval below minimum")
        self._definitions[definition.connector_id] = definition

    def definitions(self) -> tuple[ConnectorDefinition, ...]:
        return tuple(sorted(self._definitions.values(), key=lambda item: item.connector_id))

    def health_snapshot(self, states: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
        snapshot: list[dict[str, Any]] = []
        for definition in self.definitions():
            state = states.get(definition.connector_id, {})
            snapshot.append(
                {
                    "id": definition.connector_id,
                    "title": definition.title,
                    "source_type": definition.source_type,
                    "reliability": definition.reliability,
                    "enabled": state.get("enabled", definition.enabled_by_default),
                    "last_success": state.get("last_success"),
                    "last_error": state.get("last_error"),
                    "consecutive_failures": int(state.get("consecutive_failures", 0)),
                    "healthy": int(state.get("consecutive_failures", 0)) < 3,
                    "generated_at": datetime.utcnow().isoformat(),
                }
            )
        return snapshot
