from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_threat_intelligence_screenshot.py"
WORKFLOW = ROOT / ".github/workflows/documentation-screenshots.yml"
MIGRATION = ROOT / "docs/visual/screenshots/CANONICAL_CAPTURE_MIGRATION.md"


def test_threat_intelligence_capture_uses_canonical_route_and_deep_journey():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'THREAT_INTELLIGENCE_ROUTE = "/workbench/intelligence"' in text
    assert 'name="Threat Intelligence"' in text
    assert 'name="Recent canonical intelligence"' in text
    assert 'name="Provenance chain"' in text
    assert '"review_authority_proven": False' in text
    assert '"share_authority_proven": False' in text
    assert 'data-view-panel=' not in text


def test_screenshot_gate_requires_canonical_threat_intelligence_artifact():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "capture_canonical_threat_intelligence_screenshot.py" in workflow
    assert "threat-intelligence-workbench.png" in workflow
    assert 'threat_metadata.get("canonical_route") != "/workbench/intelligence"' in workflow
    assert '"review_authority_proven", "share_authority_proven"' in workflow


def test_migration_record_keeps_ui02_candidate_unpromoted_until_review():
    migration = MIGRATION.read_text(encoding="utf-8")
    assert "Canonical Threat Intelligence replacement candidate" in migration
    assert "`/workbench/intelligence`" in migration
    assert "must not replace `intelligence-workspace.png` until" in migration
