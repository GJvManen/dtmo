from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE = ROOT / "docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md"


def test_phase11_10q_records_owner_authorized_closure_before_candidate_validation():
    text = ACCEPTANCE.read_text(encoding="utf-8")
    required = [
        "MERGED / OWNER-AUTHORIZED MERGE",
        "Historical owner rejection — 2026-08-24",
        "Framework integrations",
        "Threat Intelligence",
        "IOC Explorer",
        "Knowledge Graph",
        "Vulnerability & Exposure Center",
        "Investigations",
        "Analysis & Enrichment",
        "Sharing & Exchange",
        "Automation & Playbooks",
        "Sources & Collection",
        "Operations",
        "Administration",
        "Manual UUID entry is not an acceptable primary path",
        "Empty-state-only screens",
        "owner explicitly directed the merge",
        "zero failed pull-request workflow runs",
        "freeze a new candidate",
        "production-equivalent validation",
        "independent external assurance",
    ]
    for marker in required:
        assert marker in text


def test_phase11_10q_closure_does_not_promote_repository_acceptance_to_external_evidence():
    text = ACCEPTANCE.read_text(encoding="utf-8")
    assert "BLOCKED / OWNER FUNCTIONAL REJECTION" not in text
    assert "PASS / FUNCTIONALLY_ACCEPTED" not in text
    assert "does **not** invent or retroactively create live, staging, production-equivalent" in text
    assert "Repository-controlled CI and browser gates remain repository evidence only" in text
    assert "must not reuse prior production-equivalent or external-assurance evidence" in text
