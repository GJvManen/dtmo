from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

from dtmo.scheduler import _automatic_source_due, _automatic_source_eligibility

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/CollectionWorkspace.tsx"
API = ROOT / "backend/dtmo/admin_sources.py"
SOURCE_CENTER = ROOT / "backend/dtmo/source_center.py"
SCHEDULER = ROOT / "backend/dtmo/scheduler.py"


def test_collection_workspace_exposes_complete_same_origin_operator_journey() -> None:
    text = WORKSPACE.read_text(encoding="utf-8")
    for marker in (
        "'/api/v1/admin/sources'",
        "'/api/v1/admin/sources/catalog'",
        "'/api/v1/admin/sources/catalog/bootstrap'",
        "'/api/v1/source-center/status'",
        "Register source",
        "Register disabled source",
        "'PATCH'",
        "'validate'",
        "'test'",
        "'run'",
        "credentials: 'same-origin'",
        "manage:connectors",
        "Reference only; never enter a raw API key or password.",
        "All registered sources",
    ):
        assert marker in text


def test_collection_workspace_exposes_supported_builtin_clean_install_path() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    source_center = SOURCE_CENTER.read_text(encoding="utf-8")

    for marker in (
        "supported-built-in",
        "manual load available",
        "Load CISA KEV now",
        "builtInRun",
        "`/connectors/${encodeURIComponent(sourceId)}/run`",
        "Manual loading is blocked in this environment",
        "DTMO does not bypass that boundary from the browser",
    ):
        assert marker in workspace

    assert 'entry.execution_status == "supported-built-in"' in source_center
    assert '"manual_run_available"' in source_center
    assert "(not settings.production or settings.feature_live_connectors)" in source_center
    assert "feature_live_connectors = True" not in workspace


def test_collection_api_supports_registration_activation_validation_test_and_run() -> None:
    text = API.read_text(encoding="utf-8")
    for marker in (
        '@router.post("", response_model=SourceResponse',
        '@router.patch("/{source_id}"',
        '@router.post("/{source_id}/validate")',
        '@router.post("/{source_id}/test")',
        '@router.post("/{source_id}/run")',
        '@router.post("/catalog/bootstrap"',
        "Permission.MANAGE_CONNECTORS",
        "new manual sources must be created disabled",
        "source registry changes require a human admin role",
        "publication_gate",
    ):
        assert marker in text


def test_enabled_supported_sources_are_reconciled_automatically() -> None:
    text = SCHEDULER.read_text(encoding="utf-8")
    for marker in (
        "registered-source-reconciliation",
        "reconcile_registered_sources",
        "automatic-interval",
        "source.auto-run",
        "service:source-scheduler",
        "human-review-and-separate-share-approval-required",
        "ConnectorStateStore",
        "interval_seconds",
        "is_isolated",
    ):
        assert marker in text

    ready = SimpleNamespace(id="nvd-cve", source_type="json-feed", enabled=True, secret_ref=None)
    assert _automatic_source_eligibility(ready) == (True, "ready")

    disabled = SimpleNamespace(id="nvd-cve", source_type="json-feed", enabled=False, secret_ref=None)
    assert _automatic_source_eligibility(disabled) == (False, "disabled")

    research_only = SimpleNamespace(id="enisa-threat-landscape", source_type="json-feed", enabled=True, secret_ref=None)
    assert _automatic_source_eligibility(research_only) == (False, "unsupported-or-research-only")

    credential_missing = SimpleNamespace(id="cisco-security-advisories", source_type="json-feed", enabled=True, secret_ref=None)
    assert _automatic_source_eligibility(credential_missing) == (False, "credential-reference-required")


def test_automatic_collection_respects_each_source_interval() -> None:
    now = datetime(2026, 8, 25, 12, 0, tzinfo=UTC)
    assert _automatic_source_due(None, interval_seconds=3600, now=now) is True
    recent = SimpleNamespace(updated_at=now - timedelta(seconds=3599))
    assert _automatic_source_due(recent, interval_seconds=3600, now=now) is False
    due = SimpleNamespace(updated_at=now - timedelta(seconds=3600))
    assert _automatic_source_due(due, interval_seconds=3600, now=now) is True


def test_collection_evidence_boundary_remains_fail_closed() -> None:
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "Connectivity, successful testing or ingestion proves only the recorded collection action" in text
    assert "Neither proves source truth, compromise, review completion, external-share authority, production readiness or publication authorization" in text
