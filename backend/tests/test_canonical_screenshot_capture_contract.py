from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_workbench_screenshots.py"
WORKFLOW = ROOT / ".github/workflows/documentation-screenshots.yml"
CATALOGUE = ROOT / "docs/visual/screenshots/README.md"


def test_command_center_capture_uses_canonical_workbench_route():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'COMMAND_CENTER_ROUTE = "/workbench/command-center"' in text
    assert 'data-view-panel="overview"' not in text
    assert 'get_by_role("button", name="Intelligence"' not in text
    assert '"live_connectivity_proven": False' in text
    assert '"owner_acceptance_proven": False' in text
    assert '"production_equivalent_proven": False' in text


def test_screenshot_gate_requires_canonical_command_center_artifact():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "capture_canonical_workbench_screenshots.py" in workflow
    assert "command-center-workbench.png" in workflow
    assert 'canonical_metadata.get("canonical_route") != "/workbench/command-center"' in workflow


def test_catalogue_keeps_candidate_unpromoted_until_review():
    catalogue = CATALOGUE.read_text(encoding="utf-8")
    assert "Canonical Command Center replacement candidate" in catalogue
    assert "generated / review required before promotion" in catalogue
    assert "must not replace `overview-dashboard.png` until" in catalogue
