from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_governance_workspace_is_wired_to_canonical_route() -> None:
    app = read("frontend/src/App.tsx")
    workspace = read("frontend/src/GovernanceWorkspace.tsx")
    assert "import { GovernanceWorkspace }" in app
    assert "workspace.path === '/governance'" in app
    assert "<GovernanceWorkspace />" in app
    assert "/api/v1/governance/knowledge" in workspace


def test_governance_framework_claims_use_explicit_crosswalk_and_fail_closed() -> None:
    backend = read("backend/dtmo/governance_knowledge.py")
    crosswalk = read("backend/dtmo/governance_crosswalk.py")
    workspace = read("frontend/src/GovernanceWorkspace.tsx").lower()
    architecture = read("docs/architecture/PHASE11_10L_GOVERNANCE_EVIDENCE.md").lower()
    user = read("docs/user/GOVERNANCE_EVIDENCE_WORKSPACE.md").lower()
    assert "control_crosswalk" in backend
    assert '"coverage": "mapped_internal"' in backend
    assert 'coverage = "mapped_partial"' in backend
    assert 'coverage = "context_only"' in backend
    for marker in ("ID.02", "SM.07", "T1078", "T1087", "CVSS:4.0"):
        assert marker in crosswalk
    assert "no inferred crosswalks" in workspace
    assert "mapping visibility ≠ compliance approval" in workspace
    assert "typed control crosswalk" in workspace
    assert "provenance:" in workspace
    assert "implementation:" in workspace
    assert "data-governance-control" in workspace
    assert "normenkader ibp" in architecture
    assert "mitre att&ck" in architecture
    assert "nist csf" in architecture
    assert "cvss" in architecture
    assert "partial" in architecture
    assert "does not prove compliance" in user


def test_governance_evidence_preserves_authority_and_assurance_boundaries() -> None:
    workspace = read("frontend/src/GovernanceWorkspace.tsx").lower()
    qa = read("docs/qa/PHASE11_10L_GOVERNANCE_EVIDENCE_GATE.md").lower()
    for phrase in (
        "review",
        "share",
        "publication",
        "production authority",
    ):
        assert phrase in workspace
    assert "repository-controlled exact-head evidence only" in qa
    assert "no-go / blocked — platform industrialisation required" in qa
