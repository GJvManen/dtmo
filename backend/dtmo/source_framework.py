from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from dtmo.apple_adapter import APPLE_EXECUTION_PROFILE, execute_apple_source
from dtmo.chrome_adapter import CHROME_EXECUTION_PROFILE, execute_chrome_source
from dtmo.connectors.base import ConnectorResult
from dtmo.credentialed_source_executor import (
    CREDENTIALED_EXECUTION_PROFILES,
    execute_credentialed_source,
)
from dtmo.redhat_adapter import REDHAT_EXECUTION_PROFILE, execute_redhat_source
from dtmo.source_catalog import SOURCE_CATALOG, catalog_by_id
from dtmo.source_executor import (
    SUPPORTED_REGISTRY_EXECUTION_PROFILES,
    SourceExecutionError,
    execute_registered_source,
)
from dtmo.sources import SourceDefinition

ExecutionKind = Literal["anonymous", "credentialed"]


@dataclass(frozen=True, slots=True)
class SourceAdapterSpec:
    profile: str
    execution_kind: ExecutionKind
    requires_secret: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class SourceAdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, SourceAdapterSpec] = {}

    def register(self, spec: SourceAdapterSpec) -> None:
        if spec.profile in self._adapters:
            raise ValueError(f"duplicate source adapter profile: {spec.profile}")
        self._adapters[spec.profile] = spec

    def get(self, profile: str) -> SourceAdapterSpec | None:
        return self._adapters.get(profile)

    def profiles(self) -> frozenset[str]:
        return frozenset(self._adapters)

    def specs(self) -> tuple[SourceAdapterSpec, ...]:
        return tuple(self._adapters[key] for key in sorted(self._adapters))


def _build_registry() -> SourceAdapterRegistry:
    registry = SourceAdapterRegistry()
    anonymous_profiles = set(SUPPORTED_REGISTRY_EXECUTION_PROFILES)
    anonymous_profiles.update(
        {REDHAT_EXECUTION_PROFILE, APPLE_EXECUTION_PROFILE, CHROME_EXECUTION_PROFILE}
    )
    for profile in sorted(anonymous_profiles):
        registry.register(
            SourceAdapterSpec(
                profile=profile,
                execution_kind="anonymous",
                requires_secret=False,
            )
        )
    for profile in sorted(CREDENTIALED_EXECUTION_PROFILES):
        registry.register(
            SourceAdapterSpec(
                profile=profile,
                execution_kind="credentialed",
                requires_secret=True,
            )
        )
    return registry


SOURCE_ADAPTER_REGISTRY = _build_registry()


def validate_source_framework_contract() -> None:
    supported_profiles = {
        entry.execution_profile
        for entry in SOURCE_CATALOG
        if entry.execution_status == "supported"
    }
    registered_profiles = SOURCE_ADAPTER_REGISTRY.profiles()
    if supported_profiles != registered_profiles:
        missing = sorted(supported_profiles - registered_profiles)
        orphaned = sorted(registered_profiles - supported_profiles)
        raise SourceExecutionError(
            f"source framework/catalog mismatch; missing={missing}; orphaned={orphaned}"
        )


async def execute_source(
    source: SourceDefinition, *, timeout_seconds: float = 20.0
) -> ConnectorResult:
    catalog = catalog_by_id(source.id)
    if catalog is None or catalog.execution_status != "supported":
        return await execute_registered_source(source, timeout_seconds=timeout_seconds)

    spec = SOURCE_ADAPTER_REGISTRY.get(catalog.execution_profile)
    if spec is None:
        raise SourceExecutionError(
            f"source execution profile is not registered: {catalog.execution_profile}"
        )
    if spec.requires_secret and not source.secret_ref:
        raise SourceExecutionError("credentialed source requires a secret reference")
    if spec.execution_kind == "credentialed":
        return await execute_credentialed_source(source, timeout_seconds=timeout_seconds)
    if spec.profile == REDHAT_EXECUTION_PROFILE:
        return await execute_redhat_source(source, timeout_seconds=timeout_seconds)
    if spec.profile == APPLE_EXECUTION_PROFILE:
        return await execute_apple_source(source, timeout_seconds=timeout_seconds)
    if spec.profile == CHROME_EXECUTION_PROFILE:
        return await execute_chrome_source(source, timeout_seconds=timeout_seconds)
    return await execute_registered_source(source, timeout_seconds=timeout_seconds)


def source_adapter_inventory() -> list[dict[str, object]]:
    return [spec.as_dict() for spec in SOURCE_ADAPTER_REGISTRY.specs()]
