from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_visual_analytics_screenshot.py"
WORKFLOW = ROOT / ".github/workflows/canonical-visual-analytics-screenshot.yml"
RUN_RECORD = ROOT / "docs/development/runs/RUN-20260827-374.md"


def test_visual_analytics_capture_uses_canonical_route_and_accessible_journey():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'ANALYTICS_ROUTE = "/workbench/analytics"' in text
    assert 'name="Visual Analytics"' in text
    assert 'name="Intelligence arrivals · 7 days"' in text
    assert 'name="Severity distribution"' in text
    assert 'name="Vulnerability observations"' in text
    assert 'name="Intelligence arrivals · 7 days table"' in text
    assert 'name="Severity distribution table"' in text
    assert 'name="Vulnerability observations table"' in text
    assert '"fixture_backed": True' in text
    assert '"credential_value_exposed": False' in text
    assert '"live_connectivity_proven": False' in text
    assert '"local_exposure_proven": False' in text
    assert '"review_authority_proven": False' in text
    assert '"share_authority_proven": False' in text
    assert '"publication_authority_proven": False' in text
    assert "/ui/" not in text


def test_ui07_gate_is_exact_head_and_fail_closed():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "github.event.pull_request.head.sha || github.sha" in workflow
    assert "Verify exact-head checkout" in workflow
    assert "capture_canonical_visual_analytics_screenshot.py" in workflow
    assert "visual-analytics-workbench.png" in workflow
    assert 'metadata.get("canonical_route") != "/workbench/analytics"' in workflow
    assert 'metadata.get("fixture_backed") is not True' in workflow
    assert 'metadata.get("credential_value_exposed") is not False' in workflow
    assert '"live_connectivity_proven", "owner_acceptance_proven", "production_equivalent_proven"' in workflow
    assert '"local_exposure_proven", "review_authority_proven", "share_authority_proven", "publication_authority_proven"' in workflow


def test_ui07_run_record_keeps_candidate_unpromoted_until_review():
    text = RUN_RECORD.read_text(encoding="utf-8")
    assert "visual-analytics-workbench.png" in text
    assert "/workbench/analytics" in text
    assert "must not replace `visual-analytics.png`" in text
    assert "documentation illustration only" in text
    assert "does not prove live connectivity" in text
    assert "does not prove local exposure" in text
