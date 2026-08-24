from __future__ import annotations

from pathlib import Path

from dtmo.main import app

ROOT = Path(__file__).resolve().parents[2]


def test_ioc_inventory_is_mounted_on_server_authorized_dtmo_api() -> None:
    paths = app.openapi()["paths"]
    assert "/api/v1/iocs" in paths
    source = (ROOT / "backend/dtmo/intelowl_execution.py").read_text(encoding="utf-8")
    assert 'require_permission(Permission.READ_INTELLIGENCE)' in source
    assert "IntelOwlEnrichmentRecord.observable_value" not in source  # inventory is not search-index inference
    assert "select(IntelOwlEnrichmentRecord, IntelligenceItem)" in source
    assert "Presence does not prove maliciousness or local compromise" in source


def test_ioc_inventory_exposes_persisted_observable_fields_without_share_authority() -> None:
    source = (ROOT / "backend/dtmo/intelowl_execution.py").read_text(encoding="utf-8")
    for marker in (
        "observable_type=record.observable_type",
        "observable_value=record.observable_value",
        "handling=record.handling",
        "created_at=record.created_at",
        "external_share_authorized=record.external_share_authorized",
        "local_compromise_proven=record.local_compromise_proven",
    ):
        assert marker in source


def test_canonical_ioc_workspace_filters_and_pivots_without_manual_uuid_primary_flow() -> None:
    source = (ROOT / "frontend/src/IocExplorerWorkspace.tsx").read_text(encoding="utf-8")
    unified = (ROOT / "frontend/src/UnifiedIntelligenceWorkspace.tsx").read_text(encoding="utf-8")
    for marker in (
        "/api/v1/iocs?size=500",
        "No text-derived or synthetic IOCs",
        "Minimum confidence",
        "All types",
        "All sources",
        "new URLSearchParams({ item: record.item_id, observable_type: record.observable_type, observable_value: record.observable_value })",
        "return `/workbench/analysis?${params.toString()}`",
        "return `/workbench/intelligence?item=${encodeURIComponent(record.item_id)}`",
        "Open source intelligence",
        "/workbench/intelligence/graph?item=",
        "/workbench/investigations?item=",
        "IOC inventory without inferred verdicts",
    ):
        assert marker in source
    for marker in (
        "new URLSearchParams(window.location.search).get('item')",
        "`/api/v1/intelligence/${encodeURIComponent(initialItem)}/workspace`",
        "setSelectedId(item.id); setDetail(item)",
        "IOC and other canonical object pivots may deep-link by canonical item identifier",
    ):
        assert marker in unified
    assert "IocExplorerWorkspace" in unified
    assert "if (isIoc) return <IocExplorerWorkspace />" in unified
