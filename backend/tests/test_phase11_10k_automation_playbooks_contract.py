from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_automation_workspace_is_wired_to_canonical_route() -> None:
    app = read("frontend/src/App.tsx")
    workspace = read("frontend/src/AutomationWorkspace.tsx")
    assert "import { AutomationWorkspace }" in app
    assert "workspace.path === '/automation'" in app
    assert "<AutomationWorkspace />" in app
    assert "/health" in workspace
    assert "/connectors" in workspace
    assert "/connectors/${encodeURIComponent(id)}/run" in workspace


def test_automation_authority_and_credential_boundaries_are_explicit() -> None:
    workspace = read("frontend/src/AutomationWorkspace.tsx")
    architecture = read("docs/architecture/PHASE11_10K_AUTOMATION_PLAYBOOKS.md")
    user = read("docs/user/AUTOMATION_PLAYBOOKS_WORKSPACE.md")
    assert "manage:connectors" in workspace
    assert "service_account" in workspace
    assert "X-Request-ID" in workspace
    assert "Credentials and execution remain server-side" in workspace
    assert "browser never receives upstream connector credentials" in architecture
    assert "does not prove source truth" in user


def test_automation_does_not_infer_decision_or_production_authority() -> None:
    workspace = read("frontend/src/AutomationWorkspace.tsx").lower()
    qa = read("docs/qa/PHASE11_10K_AUTOMATION_PLAYBOOKS_GATE.md").lower()
    for phrase in (
        "does not prove source truth",
        "compromise",
        "containment",
        "remediation",
        "case creation",
        "publication authority",
        "production readiness",
        "production authorization",
    ):
        assert phrase in workspace
    assert "repository-controlled exact-head evidence only" in qa
    assert "no-go / blocked — platform industrialisation required" in qa
