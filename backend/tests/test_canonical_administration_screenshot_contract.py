from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_administration_screenshot.py"
WORKFLOW = ROOT / ".github/workflows/canonical-administration-screenshot.yml"
RUN_RECORD = ROOT / "docs/development/runs/RUN-20260827-376.md"


def test_administration_capture_uses_canonical_route_and_bounded_journey():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'ADMIN_ROUTE = "/workbench/administration"' in text
    assert 'name="Administration"' in text
    assert 'name="Governed configuration and identity"' in text
    assert 'name="Runtime configuration"' in text
    assert '"fixture_backed": True' in text
    assert '"credential_value_exposed": False' in text
    assert '"mutation_executed": False' in text
    assert '"rbac_enforcement_proven": False' in text
    assert '"token_reissue_proven": False' in text
    assert '"owner_acceptance_proven": False' in text
    assert '"production_equivalent_proven": False' in text
    assert '"independent_assurance_proven": False' in text
    assert '"review_authority_proven": False' in text
    assert '"share_authority_proven": False' in text
    assert '"production_authority_proven": False' in text
    assert 'page.goto(base_url.rstrip("/") + ADMIN_ROUTE' in text
    assert 'LEGACY_ROUTE' not in text


def test_ui09_gate_is_exact_head_and_fail_closed():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "github.event.pull_request.head.sha || github.sha" in workflow
    assert "Verify exact-head checkout" in workflow
    assert "capture_canonical_administration_screenshot.py" in workflow
    assert "administration-rbac-workbench.png" in workflow
    assert 'metadata.get("canonical_route") != "/workbench/administration"' in workflow
    assert 'metadata.get("fixture_backed") is not True' in workflow
    assert 'metadata.get("credential_value_exposed") is not False' in workflow
    assert 'metadata.get("mutation_executed") is not False' in workflow
    assert '"rbac_enforcement_proven", "token_reissue_proven"' in workflow
    assert '"owner_acceptance_proven", "production_equivalent_proven", "independent_assurance_proven"' in workflow
    assert '"review_authority_proven", "share_authority_proven", "production_authority_proven"' in workflow


def test_ui09_run_record_keeps_candidate_unpromoted_until_review():
    text = RUN_RECORD.read_text(encoding="utf-8")
    assert "administration-rbac-workbench.png" in text
    assert "/workbench/administration" in text
    assert "must not replace `administration-rbac.png`" in text
    assert "documentation illustration only" in text
    assert "does not prove RBAC enforcement" in text
    assert "does not prove token reissue" in text
