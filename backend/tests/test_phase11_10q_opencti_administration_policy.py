from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/AdministrationWorkspace.tsx"
BACKEND = ROOT / "backend/dtmo/admin_center.py"


def test_opencti_runtime_policy_is_configurable_from_canonical_administration() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")

    assert "OpenCTI entity-type allowlist" in workspace
    assert "OpenCTI checkpoint path" in workspace
    assert "opencti_allowed_entity_types" in workspace
    assert "opencti_checkpoint_path" in workspace
    assert "opencti_allowed_entity_types" in backend
    assert "opencti_checkpoint_path" in backend
    assert 'integration_id in {"ail", "intelowl", "cortex", "opencti"}' in backend
    assert "OpenCTI entity-type allowlist is only valid for the OpenCTI integration" in backend
    assert "OpenCTI checkpoint path is only valid for the OpenCTI integration" in backend
    assert "Run OpenCTI" not in workspace
