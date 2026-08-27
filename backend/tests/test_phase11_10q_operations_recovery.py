from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "frontend/src/App.tsx"
OPERATIONS = ROOT / "frontend/src/OperationsWorkspace.tsx"
OPERATIONS_API = ROOT / "backend/dtmo/operations_metrics.py"
DOC = ROOT / "docs/architecture/PHASE11_10Q_OPERATIONS_CANONICALIZATION.md"


def test_canonical_operations_route_uses_dedicated_workspace():
    app = APP.read_text(encoding="utf-8")
    assert "import { OperationsWorkspace } from './OperationsWorkspace';" in app
    assert "if (workspace.path === '/operations') return <OperationsWorkspace />;" in app


def test_operations_workspace_reads_real_same_origin_runtime_contracts_without_legacy_primary_flow():
    text = OPERATIONS.read_text(encoding="utf-8")
    for marker in (
        "'/health'",
        "'/api/v1/operations/summary'",
        "'/api/v1/operations/runtime-evidence'",
        "'/connectors'",
        'Refresh runtime observation',
        'Runtime observation ≠ production assurance',
        'Missing telemetry stays unavailable',
        'data-operations-section="connector-runtime-evidence"',
        'data-operations-section="recent-connector-runs"',
        'publication approved:',
        'to="/collection"',
        'to="/administration"',
        'to="/automation"',
    ):
        assert marker in text
    assert '/ui/' not in text
    assert 'setTimeout' not in text


def test_operations_runtime_evidence_contract_is_read_only_and_bounded():
    text = OPERATIONS_API.read_text(encoding="utf-8")
    for marker in (
        '@router.get("/runtime-evidence")',
        '"evidence_source": "dtmo-persistent-connector-runtime-state"',
        '"state_table": "connector_runtime_states"',
        '"history_table": "connector_health_events"',
        '"publish_approved": run.publish_approved',
        '"claim_boundary"',
    ):
        assert marker in text
    assert '@router.post("/runtime-evidence")' not in text
    assert 'raw_evidence' not in text


def test_operations_recovery_documentation_preserves_evidence_boundary():
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "repository-controlled operational observation",
        "persisted connector runtime state",
        "not live upstream availability evidence",
        "not owner functional acceptance",
        "not staging evidence",
        "not production-equivalent evidence",
        "not external-assurance evidence",
    ):
        assert marker in text
