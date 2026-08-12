from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from dtmo.framework_experience import _PAGE, _SCRIPT, router as experience_router
from dtmo.framework_governance import _framework_dict, router as governance_router
from dtmo.persistence.framework_models import GovernanceFramework, IntelligenceFrameworkMapping


def _framework(*, mode: str = "mapping", expected: int | None = 10) -> GovernanceFramework:
    return GovernanceFramework(
        id="example",
        name="Example",
        version="1.0",
        version_label="Example 1.0",
        kind="test",
        authority="Example Authority",
        source_url="https://example.invalid/framework",
        coverage_mode=mode,
        expected_object_count=expected,
        metadata_json={},
        last_verified_at=datetime(2026, 8, 12, tzinfo=UTC),
    )


def _mapping(*, review_state: str) -> IntelligenceFrameworkMapping:
    return IntelligenceFrameworkMapping(
        id=uuid4(),
        framework_id="example",
        framework_version="1.0",
        object_type="control",
        object_id="EX.01",
        object_title="Example control",
        intelligence_id=uuid4(),
        mapping_status="mapped",
        provenance_reference="https://example.invalid/evidence",
        confidence_score=90,
        mapping_reason="Explicit evidence-backed test mapping",
        review_state=review_state,
        created_by="reviewer-a",
        created_at=datetime(2026, 8, 12, tzinfo=UTC),
    )


def test_only_approved_explicit_mappings_count_as_coverage() -> None:
    framework = _framework(expected=10)
    summary = _framework_dict(
        framework,
        [_mapping(review_state="approved"), _mapping(review_state="pending"), _mapping(review_state="rejected")],
    )
    assert summary["status"] == "MAPPED"
    assert summary["mapped_object_count"] == 1
    assert summary["approved_mapping_count"] == 1
    assert summary["pending_mapping_count"] == 1
    assert summary["rejected_mapping_count"] == 1
    assert summary["coverage_percent"] == 10.0


def test_missing_mapping_is_unmapped_and_cvss_style_context_stays_context_only() -> None:
    assert _framework_dict(_framework(), [])["status"] == "UNMAPPED"
    assert _framework_dict(_framework(mode="context_only", expected=None), [])["status"] == "CONTEXT_ONLY"


def test_migration_seeds_verified_framework_inventory_without_inferred_crosswalks() -> None:
    migration = Path("database/migrations/versions/0010_framework_governance.py").read_text(encoding="utf-8")
    assert 'down_revision: str | None = "0009_managed_rbac_assignments"' in migration
    assert '"id": "normenkader-ibp"' in migration
    assert '"version": "2024-06-06"' in migration
    assert '"information_security_norms": 69' in migration
    assert '"privacy_norms": 25' in migration
    assert '"id": "mitre-attack"' in migration
    assert '"version": "19.1"' in migration
    assert '"id": "cvss"' in migration
    assert '"version": "4.0"' in migration
    assert '"id": "nist-csf"' in migration
    assert '"version": "2.0"' in migration
    assert "intelligence_framework_mappings" in migration


def test_framework_mapping_schema_requires_provenance_confidence_and_review_state() -> None:
    table = IntelligenceFrameworkMapping.__table__
    for column in (
        "framework_id",
        "framework_version",
        "object_type",
        "object_id",
        "intelligence_id",
        "provenance_reference",
        "confidence_score",
        "mapping_reason",
        "review_state",
        "created_by",
    ):
        assert column in table.columns


def test_framework_governance_api_exposes_inventory_drilldown_and_governed_writes() -> None:
    paths = {route.path for route in governance_router.routes}
    assert "/api/v1/governance/frameworks" in paths
    assert "/api/v1/governance/frameworks/{framework_id}" in paths
    assert "/api/v1/governance/intelligence/{intelligence_id}/framework-mappings" in paths
    assert "/api/v1/governance/framework-mappings" in paths
    assert "/api/v1/governance/framework-mappings/{mapping_id}/review" in paths
    source = Path("backend/dtmo/framework_governance.py").read_text(encoding="utf-8")
    assert source.count("Permission.REVIEW_INTELLIGENCE") >= 2
    assert 'action="framework_mapping.create"' in source
    assert 'action=f"framework_mapping.{payload.decision}"' in source
    assert "append_persistent_audit_event" in source


def test_framework_ui_shows_versions_coverage_review_and_provenance_drilldown() -> None:
    assert 'id="framework-governance"' in _PAGE
    assert 'id="framework-summary"' in _PAGE
    assert 'id="framework-cards"' in _PAGE
    assert "UNMAPPED" in _PAGE
    assert "provenance" in _PAGE.lower()
    assert "/ui/framework-experience.js" in _PAGE
    assert "/api/v1/governance/frameworks" in _SCRIPT
    assert "pending_mapping_count" in _SCRIPT
    assert "approved_mapping_count" in _SCRIPT
    assert "provenance_reference" in _SCRIPT
    assert "intelligence_title" in _SCRIPT
    assert "Geen expliciete mappings beschikbaar" in _SCRIPT


def test_framework_composer_preserves_trends_severity_rbac_and_legacy_governance() -> None:
    assert 'data-trend-surface="overview"' in _PAGE
    assert 'data-severity-filter' in _PAGE
    assert 'id="rbac-administration"' in _PAGE
    assert 'id="governance-knowledge"' in _PAGE
    routes = [route for route in experience_router.routes if route.path in {"/", "/ui/console"}]
    assert {route.path for route in routes} == {"/", "/ui/console"}
