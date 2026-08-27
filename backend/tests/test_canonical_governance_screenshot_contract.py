from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_governance_screenshot.py"
WORKFLOW = ROOT / ".github/workflows/canonical-governance-screenshot.yml"
RUN_RECORD = ROOT / "docs/development/runs/RUN-20260827-375.md"


def test_governance_capture_uses_canonical_route_and_explicit_mapping_journey():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'GOVERNANCE_ROUTE = "/workbench/governance"' in text
    assert 'name="Governance & Evidence"' in text
    assert 'name="Explicit coverage state"' in text
    assert '"Normenkader IBP"' in text
    assert '"MITRE ATT&CK"' in text
    assert '"NIST CSF"' in text
    assert '"CVSS"' in text
    assert '"DTMO-TVM-01"' in text
    assert '"SM.07"' in text
    assert '"fixture_backed": True' in text
    assert '"credential_value_exposed": False' in text
    assert '"compliance_proven": False' in text
    assert '"certification_proven": False' in text
    assert '"control_effectiveness_proven": False' in text
    assert '"independent_assurance_proven": False' in text
    assert '"review_authority_proven": False' in text
    assert '"share_authority_proven": False' in text
    assert '"administration_authority_proven": False' in text
    assert '"production_authority_proven": False' in text
    assert 'page.goto(base_url.rstrip("/") + GOVERNANCE_ROUTE' in text
    assert '"/ui/governance"' not in text
    assert "LEGACY_ROUTE" not in text


def test_ui08_gate_is_exact_head_and_fail_closed():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "github.event.pull_request.head.sha || github.sha" in workflow
    assert "Verify exact-head checkout" in workflow
    assert "capture_canonical_governance_screenshot.py" in workflow
    assert "governance-evidence-workbench.png" in workflow
    assert 'metadata.get("canonical_route") != "/workbench/governance"' in workflow
    assert 'metadata.get("fixture_backed") is not True' in workflow
    assert 'metadata.get("credential_value_exposed") is not False' in workflow
    assert '"compliance_proven", "certification_proven", "control_effectiveness_proven"' in workflow
    assert '"owner_acceptance_proven", "production_equivalent_proven", "independent_assurance_proven"' in workflow
    assert '"review_authority_proven", "share_authority_proven", "administration_authority_proven", "production_authority_proven"' in workflow


def test_ui08_run_record_keeps_candidate_unpromoted_until_review():
    text = RUN_RECORD.read_text(encoding="utf-8")
    assert "governance-evidence-workbench.png" in text
    assert "/workbench/governance" in text
    assert "must not replace `governance-frameworks.png`" in text
    assert "documentation illustration only" in text
    assert "does not prove compliance" in text
    assert "does not prove independent assurance" in text
