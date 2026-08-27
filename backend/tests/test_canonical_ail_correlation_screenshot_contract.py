from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_ail_correlation_screenshot.py"
WORKFLOW = ROOT / ".github/workflows/documentation-screenshots.yml"
MIGRATION = ROOT / "docs/visual/screenshots/CANONICAL_CAPTURE_MIGRATION.md"


def test_ail_capture_uses_canonical_ioc_explorer_and_read_only_journey():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'IOC_ROUTE = "/workbench/intelligence/iocs"' in text
    assert 'name="IOC Explorer"' in text
    assert 'name="Inspect AIL correlation"' in text
    assert 'name="AIL correlation context"' in text
    assert '"raw_content_exposed": False' in text
    assert '"analysis_only": True' in text
    assert '"credential_value_exposed": False' in text
    assert '"review_authority_proven": False' in text
    assert '"share_authority_proven": False' in text
    assert '"case_authority_proven": False' in text
    assert '"publication_authority_proven": False' in text
    assert "/ui/intelligence-workspace" not in text
    assert "data-view-panel=" not in text


def test_screenshot_gate_requires_canonical_ail_candidate_and_boundaries():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "capture_canonical_ail_correlation_screenshot.py" in workflow
    assert "ail-correlation-workbench.png" in workflow
    assert 'ail_metadata.get("canonical_route") != "/workbench/intelligence/iocs"' in workflow
    assert 'ail_metadata.get("raw_content_exposed") is not False' in workflow
    assert 'ail_metadata.get("analysis_only") is not True' in workflow
    assert 'ail_metadata.get("credential_value_exposed") is not False' in workflow
    assert '"review_authority_proven", "share_authority_proven", "case_authority_proven", "publication_authority_proven"' in workflow


def test_migration_record_keeps_ui06_candidate_unpromoted_until_review():
    migration = MIGRATION.read_text(encoding="utf-8")
    assert "Canonical AIL correlation replacement candidate" in migration
    assert "must not replace `ail-correlation-workspace.png` until" in migration
    assert "raw_content_exposed = false" in migration
    assert "analysis_only = true" in migration
    assert "credential_value_exposed = false" in migration
