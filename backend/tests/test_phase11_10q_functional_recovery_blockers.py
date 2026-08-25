from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE = ROOT / "docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md"


def test_phase11_10q_remains_blocked_while_owner_rejected_workspaces_are_unresolved():
    text = ACCEPTANCE.read_text(encoding="utf-8")
    required = [
        "BLOCKED / OWNER FUNCTIONAL REJECTION",
        "Framework integrations | BLOCKED",
        "Threat Intelligence | BLOCKED",
        "IOC Explorer | BLOCKED",
        "Knowledge Graph | BLOCKED",
        "Vulnerability & Exposure Center | BLOCKED",
        "Investigations | BLOCKED",
        "Analysis & Enrichment | BLOCKED",
        "Sharing & Exchange | BLOCKED",
        "Automation & Playbooks | BLOCKED",
        "Sources & Collection | BLOCKED",
        "Operations | BLOCKED",
        "Administration | BLOCKED",
        "An empty-state-only workspace is not functionally complete",
        "Manual UUID entry is not an acceptable primary workflow",
        "owner functional retest explicitly accepts the canonical interface",
    ]
    for marker in required:
        assert marker in text


def test_phase11_10q_cannot_claim_pass_while_any_hard_blocker_is_blocked():
    text = ACCEPTANCE.read_text(encoding="utf-8")
    blocker_rows = [line for line in text.splitlines() if "| BLOCKED |" in line]
    assert len(blocker_rows) >= 10
    assert "PASS / FUNCTIONALLY_ACCEPTED" not in text
