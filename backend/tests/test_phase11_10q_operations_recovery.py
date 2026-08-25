from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "frontend/src/App.tsx"
OPERATIONS = ROOT / "frontend/src/OperationsWorkspace.tsx"
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
        "'/connectors'",
        'Refresh runtime observation',
        'Runtime observation ≠ production assurance',
        'Missing telemetry stays unavailable',
        'to="/collection"',
        'to="/administration"',
        'to="/automation"',
    ):
        assert marker in text
    assert '/ui/' not in text
    assert 'setTimeout' not in text


def test_operations_recovery_documentation_preserves_evidence_boundary():
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "repository-controlled operational observation",
        "not owner functional acceptance",
        "not staging evidence",
        "not production-equivalent evidence",
        "not external-assurance evidence",
    ):
        assert marker in text
