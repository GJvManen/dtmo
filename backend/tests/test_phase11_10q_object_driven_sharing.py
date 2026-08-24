from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend" / "src" / "MispSharingWorkspace.tsx"


def test_sharing_discovers_canonical_targets_without_uuid_primary_flow():
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "'/api/v1/command-center'" in source
    assert "recent_intelligence" in source
    assert "Canonical target discovery" in source
    assert "Select intelligence for sharing review" in source
    assert "Advanced deep link / troubleshooting" in source
    assert "Canonical intelligence item UUID" in source


def test_object_selection_loads_governed_sharing_state():
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "onClick={() => void loadState(item.id)}" in source
    assert "`/api/v1/sharing/items/${encodeURIComponent(id)}`" in source
    assert "Record review" in source
    assert "Approve sharing" in source
    assert "Export approved intelligence" in source


def test_sharing_recovery_preserves_authority_and_fail_closed_boundaries():
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "does not grant review, sharing, publication or synchronization authority" in source
    assert "No empty-object, MISP-health or sharing-readiness conclusion is inferred" in source
    assert "published=false" in source
    assert "Publication authority: no" in source
    assert "Synchronization authority: no" in source
