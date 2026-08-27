from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_sources_collection_screenshot.py"
WORKFLOW = ROOT / ".github/workflows/documentation-screenshots.yml"
MIGRATION = ROOT / "docs/visual/screenshots/CANONICAL_CAPTURE_MIGRATION.md"


def test_sources_collection_capture_uses_canonical_route_and_read_only_journey():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'COLLECTION_ROUTE = "/workbench/collection"' in text
    assert 'name="Sources & Collection"' in text
    assert 'name="Code-reviewed source profiles"' in text
    assert 'has_text="CISA KEV"' in text
    assert '"connector_execution_proven": False' in text
    assert '"source_activation_authority_proven": False' in text
    assert '"publication_authority_proven": False' in text
    assert '"credential_value_exposed": False' in text
    assert 'data-view-panel=' not in text


def test_screenshot_gate_requires_canonical_sources_collection_artifact():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "capture_canonical_sources_collection_screenshot.py" in workflow
    assert "sources-collection-workbench.png" in workflow
    assert 'collection_metadata.get("canonical_route") != "/workbench/collection"' in workflow
    assert '"connector_execution_proven", "source_activation_authority_proven", "publication_authority_proven"' in workflow
    assert 'collection_metadata.get("credential_value_exposed") is not False' in workflow


def test_migration_record_keeps_ui03_candidate_unpromoted_until_review():
    migration = MIGRATION.read_text(encoding="utf-8")
    assert "Canonical Sources & Collection replacement candidate" in migration
    assert "must not replace `sources-catalogue.png` until" in migration
    assert "connector_execution_proven = false" in migration
    assert "credential_value_exposed = false" in migration
