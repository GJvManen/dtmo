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


def test_integration_capabilities_never_infer_runtime_health() -> None:
    settings = Settings(
        _env_file=None,
        feature_live_connectors=True,
        feature_taranis_connector=True,
        taranis_api_base="https://taranis.example.invalid/api",
        feature_intelowl_enrichment=True,
        intelowl_api_base="https://intelowl.example.invalid/api",
    )
    capabilities = build_integration_capabilities(settings)
    taranis = next(item for item in capabilities if item["id"] == "taranis")
    intelowl = next(item for item in capabilities if item["id"] == "intelowl")

    assert taranis["state"] == "enabled"
    assert taranis["scheduled_collection"] is True
    assert taranis["runtime_observation"] is None
    assert taranis["runtime_health_claim"] is False
    assert intelowl["state"] == "enabled"
    assert intelowl["runtime_health_claim"] is False


def test_enabled_but_unconfigured_integration_fails_closed() -> None:
    settings = Settings(_env_file=None, feature_cortex_analysis=True, cortex_api_base="")
    cortex = next(
        item for item in build_integration_capabilities(settings) if item["id"] == "cortex"
    )
    assert cortex["state"] == "configuration-required"
    assert cortex["configured"] is False
    assert cortex["runtime_health_claim"] is False


class _FailingSession:
    async def scalar(self, *_args: object, **_kwargs: object) -> object:
        raise RuntimeError("canonical store unavailable")

    async def rollback(self) -> None:
        return None


@pytest.mark.asyncio
async def test_canonical_store_failure_never_synthesizes_zero_metrics() -> None:
    snapshot = await build_command_center_snapshot(
        cast(Any, _FailingSession()),
        Settings(_env_file=None),
    )
    assert snapshot["data_state"] == "unavailable"
    assert snapshot["recent_intelligence"] == []
    assert all(metric["value"] is None for metric in snapshot["metrics"])
    assert "rather than synthesized" in snapshot["evidence_boundary"]


def test_frontend_command_center_uses_governed_api_and_explicit_boundaries() -> None:
    app_source = (ROOT / "frontend/src/App.tsx").read_text(encoding="utf-8")
    styles = (ROOT / "frontend/src/command-center.css").read_text(encoding="utf-8")
    api_source = (ROOT / "backend/dtmo/api_command_center.py").read_text(encoding="utf-8")

    for marker in (
        "/api/v1/command-center",
        "Command Center",
        "Canonical data unavailable",
        "No inferred health",
        "Visibility ≠ authority",
        "Operational visibility without synthetic claims",
    ):
        assert marker in app_source
    assert "Permission.READ_INTELLIGENCE" in api_source
    assert "runtime_health_claim" in app_source
    assert ".kpi-grid" in styles
    assert ".integration-list" in styles
    assert ".workflow-strip" in styles


def test_phase11_10c_documentation_and_gate_are_discoverable() -> None:
    expected = (
        "docs/architecture/PHASE11_10C_COMMAND_CENTER.md",
        "docs/qa/PHASE11_10C_COMMAND_CENTER_GATE.md",
        ".github/workflows/phase11-command-center.yml",
    )
    for relative in expected:
        assert (ROOT / relative).is_file(), relative
