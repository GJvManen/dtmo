from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_sharing_exchange_screenshot.py"
WORKFLOW = ROOT / ".github/workflows/documentation-screenshots.yml"
MIGRATION = ROOT / "docs/visual/screenshots/CANONICAL_CAPTURE_MIGRATION.md"


def test_sharing_capture_uses_canonical_route_and_governed_journey():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'SHARING_ROUTE = "/workbench/sharing"' in text
    assert 'name="Sharing & Exchange"' in text
    assert 'name="Create unpublished event"' in text
    assert 'name="Authoritative source constraints"' in text
    assert 'name="MISP export history"' in text
    assert '"human_review_executed": False' in text
    assert '"share_approval_executed": False' in text
    assert '"misp_export_executed": False' in text
    assert '"publication_authority_proven": False' in text
    assert '"synchronization_authority_proven": False' in text
    assert '"credential_value_exposed": False' in text


def test_screenshot_workflow_validates_canonical_sharing_claim_boundaries():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "capture_canonical_sharing_exchange_screenshot.py" in workflow
    assert "sharing-exchange-workbench.png" in workflow
    assert 'canonical_route") != "/workbench/sharing"' in workflow
    for claim in (
        "human_review_executed",
        "share_approval_executed",
        "misp_export_executed",
        "publication_authority_proven",
        "synchronization_authority_proven",
    ):
        assert claim in workflow


def test_migration_record_keeps_ui05_candidate_unpromoted_until_review():
    migration = MIGRATION.read_text(encoding="utf-8")
    assert "Canonical Sharing & Exchange replacement candidate" in migration
    assert "must not replace `misp-governed-workflow.png` until" in migration
    assert "independent review" in migration
    assert "separate share approval" in migration
    assert "unpublished MISP export" in migration
    assert "publication authority" in migration
    assert "synchronization authority" in migration
