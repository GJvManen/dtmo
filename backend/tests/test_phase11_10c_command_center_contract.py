from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pytest

from dtmo.command_center import build_command_center_snapshot, build_integration_capabilities
from dtmo.config import Settings
from dtmo.main import app

ROOT = Path(__file__).resolve().parents[2]


def test_command_center_route_is_mounted_in_canonical_api() -> None:
    assert "/api/v1/command-center" in app.openapi()["paths"]


def test_integration_capabilities_reuse_governed_readiness_and_never_infer_runtime_health() -> None:
    settings = Settings(
        _env_file=None,
        feature_live_connectors=True,
        feature_taranis_connector=True,
        taranis_api_base="https://taranis.example.invalid/api",
        taranis_api_token="runtime-token",
        feature_intelowl_enrichment=True,
        intelowl_api_base="https://intelowl.example.invalid/api",
    )
    capabilities = build_integration_capabilities(settings)
    taranis = next(item for item in capabilities if item["id"] == "taranis")
    intelowl = next(item for item in capabilities if item["id"] == "intelowl")

    assert taranis["state"] == "enabled"
    assert taranis["scheduled_collection"] is True
    assert taranis["activation_blockers"] == []
    assert taranis["runtime_observation"] is None
    assert taranis["runtime_health_claim"] is False
    assert intelowl["state"] == "configuration-required"
    assert "server-side credential" in intelowl["activation_blockers"]
    assert "IntelOwl analyzer allowlist" in intelowl["activation_blockers"]
    assert intelowl["runtime_health_claim"] is False


def test_command_center_maps_disabled_capabilities_to_actionable_administration_state() -> None:
    settings = Settings(
        _env_file=None,
        feature_opencti_read=False,
        opencti_api_base="https://opencti.example.invalid/graphql",
        opencti_api_token="runtime-token",
        opencti_allowed_entity_types="Indicator,Malware",
        opencti_checkpoint_path="state/opencti-checkpoint.json",
    )
    opencti = next(
        item for item in build_integration_capabilities(settings) if item["id"] == "opencti"
    )
    assert opencti["enabled"] is False
    assert opencti["readiness_state"] == "disabled"
    assert opencti["can_activate"] is True
    assert opencti["activation_blockers"] == []
    assert opencti["state"] == "configuration-required"
    assert "explicit governed activation" in opencti["detail"]
    assert opencti["runtime_health_claim"] is False


def test_command_center_includes_ail_and_fails_closed_on_component_specific_readiness() -> None:
    settings = Settings(
        _env_file=None,
        feature_ail_connector=True,
        ail_api_base="https://ail.example.invalid/api",
        ail_api_key="runtime-secret",
    )
    rows = {item["id"]: item for item in build_integration_capabilities(settings)}
    assert {"misp", "ail", "taranis", "intelowl", "cortex", "opencti", "thehive"} <= rows.keys()
    assert rows["ail"]["state"] == "configuration-required"
    assert rows["ail"]["credential_configured"] is True
    assert rows["ail"]["can_activate"] is False
    assert rows["ail"]["activation_blockers"] == ["AIL object scope"]


def test_enabled_but_unconfigured_integration_fails_closed() -> None:
    settings = Settings(_env_file=None, feature_cortex_analysis=True, cortex_api_base="")
    cortex = next(
        item for item in build_integration_capabilities(settings) if item["id"] == "cortex"
    )
    assert cortex["state"] == "configuration-required"
    assert cortex["configured"] is False
    assert "API endpoint" in cortex["activation_blockers"]
    assert "server-side credential" in cortex["activation_blockers"]
    assert "Cortex analyzer allowlist" in cortex["activation_blockers"]
    assert cortex["runtime_health_claim"] is False


class _FailingSession:
    async def scalar(self, *_args: object, **_kwargs: object) -> object:
        raise RuntimeError("canonical store unavailable")

    async def rollback(self) -> None:
        return None


@pytest.mark.asyncio
async def test_canonical_store_failure_never_synthesizes_zero_metrics_or_trends() -> None:
    snapshot = await build_command_center_snapshot(
        cast(Any, _FailingSession()),
        Settings(_env_file=None),
    )
    assert snapshot["data_state"] == "unavailable"
    assert snapshot["recent_intelligence"] == []
    assert snapshot["trends"] == {
        "intelligence_7d": [],
        "severity_distribution": [],
        "source_distribution": [],
        "type_distribution": [],
        "enrichment_status_distribution": [],
        "collection_volume_distribution": [],
        "collection_observation_age": [],
        "ioc_type_distribution": [],
        "investigation_handoff_status_distribution": [],
    }
    assert all(metric["value"] is None for metric in snapshot["metrics"])
    assert "rather than synthesized" in snapshot["evidence_boundary"]


def test_frontend_command_center_uses_governed_api_graphs_pivots_and_explicit_boundaries() -> None:
    app_source = (ROOT / "frontend/src/App.tsx").read_text(encoding="utf-8")
    styles = (ROOT / "frontend/src/command-center.css").read_text(encoding="utf-8")
    api_source = (ROOT / "backend/dtmo/api_command_center.py").read_text(encoding="utf-8")
    model_source = (ROOT / "backend/dtmo/command_center.py").read_text(encoding="utf-8")

    for marker in (
        "/api/v1/command-center",
        "Command Center",
        "Canonical data unavailable",
        "Integration readiness",
        "Intelligence arrivals · 7 days",
        "Severity composition",
        "Open administration →",
        "Inspect collection",
        "Visibility ≠ authority",
        "Operational visibility without synthetic claims",
    ):
        assert marker in app_source
    assert "Permission.READ_INTELLIGENCE" in api_source
    assert "runtime_health_claim" in app_source
    assert "integration_readiness" in model_source
    assert '"ail": "ail"' in model_source
    assert '"activation_blockers"' in model_source
    assert '"readiness_state"' in model_source
    assert '"action"' in model_source
    assert '"detail"' in model_source
    assert '"intelligence_7d"' in model_source
    assert '"severity_distribution"' in model_source
    assert '"type_distribution"' in model_source
    assert '"enrichment_status_distribution"' in model_source
    assert '"collection_volume_distribution"' in model_source
    assert '"collection_observation_age"' in model_source
    assert '"ioc_type_distribution"' in model_source
    assert '"investigation_handoff_status_distribution"' in model_source
    assert ".kpi-grid" in styles
    assert ".integration-list" in styles
    assert ".trend-chart" in styles
    assert ".severity-bars" in styles
    assert ".workflow-strip" in styles


def test_phase11_10c_documentation_and_gate_are_discoverable() -> None:
    expected = (
        "docs/architecture/PHASE11_10C_COMMAND_CENTER.md",
        "docs/qa/PHASE11_10C_COMMAND_CENTER_GATE.md",
        ".github/workflows/phase11-command-center.yml",
    )
    for relative in expected:
        assert (ROOT / relative).is_file(), relative
