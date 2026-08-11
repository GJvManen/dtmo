from __future__ import annotations

import pytest

from dtmo.connectors.base import ConnectorResult
from dtmo.source_catalog import SOURCE_CATALOG
from dtmo.source_framework import (
    SOURCE_ADAPTER_REGISTRY,
    SourceAdapterRegistry,
    SourceAdapterSpec,
    execute_source,
    source_adapter_inventory,
    validate_source_framework_contract,
)
from dtmo.source_executor import SourceExecutionError
from dtmo.sources import SourceDefinition


def _source(source_id: str, *, secret_ref: str | None = None) -> SourceDefinition:
    return SourceDefinition(
        id=source_id,
        name=source_id,
        source_type="json-feed",
        endpoint_url="https://example.com/feed",
        enabled=True,
        interval_seconds=3600,
        reliability="authoritative",
        secret_ref=secret_ref,
        created_by="admin",
        updated_by="admin",
    )


def test_every_supported_catalog_source_has_exactly_one_framework_adapter() -> None:
    validate_source_framework_contract()
    supported_profiles = {
        entry.execution_profile
        for entry in SOURCE_CATALOG
        if entry.execution_status == "supported"
    }
    assert SOURCE_ADAPTER_REGISTRY.profiles() == supported_profiles


def test_adapter_registry_rejects_duplicate_profiles() -> None:
    registry = SourceAdapterRegistry()
    spec = SourceAdapterSpec(
        profile="example-v1",
        execution_kind="anonymous",
        requires_secret=False,
    )
    registry.register(spec)
    with pytest.raises(ValueError, match="duplicate source adapter profile"):
        registry.register(spec)


def test_adapter_inventory_exposes_execution_characteristics_without_secret_values() -> None:
    inventory = source_adapter_inventory()
    assert inventory
    cisco = next(item for item in inventory if item["profile"] == "cisco-openvuln-v2")
    assert cisco == {
        "profile": "cisco-openvuln-v2",
        "execution_kind": "credentialed",
        "requires_secret": True,
    }
    assert all("secret" not in key or key == "requires_secret" for item in inventory for key in item)


@pytest.mark.asyncio
async def test_framework_dispatches_anonymous_source(monkeypatch: pytest.MonkeyPatch) -> None:
    source = _source("nvd-cve")
    expected = ConnectorResult(
        connector_id=source.id,
        started_at="start",
        finished_at="finish",
        records=[],
        attempts=1,
        status="completed",
    )

    async def fake_execute_registered_source(source_arg: SourceDefinition, *, timeout_seconds: float):
        assert source_arg is source
        assert timeout_seconds == 7.0
        return expected

    monkeypatch.setattr("dtmo.source_framework.execute_registered_source", fake_execute_registered_source)
    assert await execute_source(source, timeout_seconds=7.0) is expected


@pytest.mark.asyncio
async def test_framework_dispatches_credentialed_source(monkeypatch: pytest.MonkeyPatch) -> None:
    source = _source("cisco-security-advisories", secret_ref="env:CISCO_OPENVULN_TOKEN")
    expected = ConnectorResult(
        connector_id=source.id,
        started_at="start",
        finished_at="finish",
        records=[],
        attempts=1,
        status="completed",
    )

    async def fake_execute_credentialed_source(source_arg: SourceDefinition, *, timeout_seconds: float):
        assert source_arg is source
        assert timeout_seconds == 9.0
        return expected

    monkeypatch.setattr(
        "dtmo.source_framework.execute_credentialed_source",
        fake_execute_credentialed_source,
    )
    assert await execute_source(source, timeout_seconds=9.0) is expected


@pytest.mark.asyncio
async def test_framework_fails_closed_when_credential_reference_is_missing() -> None:
    source = _source("cisco-security-advisories")
    with pytest.raises(SourceExecutionError, match="requires a secret reference"):
        await execute_source(source)
