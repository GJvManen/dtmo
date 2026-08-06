from __future__ import annotations

from sqlalchemy import CheckConstraint, Enum, UniqueConstraint

from dtmo.intelligence.model import (
    ConfidenceLevel,
    IntelligenceSeverity,
    IntelligenceType,
    SourceReliability,
)
from dtmo.persistence.models import (
    IntelligenceItem,
    IntelligenceRevision,
    ProvenanceRecord,
)


def _constraint_names(model: type[object], constraint_type: type[object]) -> set[str]:
    return {
        constraint.name
        for constraint in model.__table__.constraints  # type: ignore[attr-defined]
        if isinstance(constraint, constraint_type) and constraint.name is not None
    }


def test_intelligence_item_uses_canonical_enum_types() -> None:
    item_type = IntelligenceItem.__table__.c.item_type.type
    severity = IntelligenceItem.__table__.c.severity.type
    confidence_level = IntelligenceItem.__table__.c.confidence_level.type

    assert isinstance(item_type, Enum)
    assert item_type.enum_class is IntelligenceType
    assert item_type.native_enum is False

    assert isinstance(severity, Enum)
    assert severity.enum_class is IntelligenceSeverity
    assert severity.native_enum is False

    assert isinstance(confidence_level, Enum)
    assert confidence_level.enum_class is ConfidenceLevel
    assert confidence_level.native_enum is False


def test_intelligence_item_enforces_score_boundaries() -> None:
    names = _constraint_names(IntelligenceItem, CheckConstraint)
    assert "ck_intelligence_confidence_score" in names
    assert "ck_intelligence_education_relevance" in names


def test_provenance_captures_source_assessment_and_deduplicates_evidence() -> None:
    reliability = ProvenanceRecord.__table__.c.source_reliability.type
    assert isinstance(reliability, Enum)
    assert reliability.enum_class is SourceReliability
    assert reliability.native_enum is False

    check_names = _constraint_names(ProvenanceRecord, CheckConstraint)
    unique_names = _constraint_names(ProvenanceRecord, UniqueConstraint)
    assert "ck_provenance_confidence_score" in check_names
    assert "uq_provenance_item_source_content" in unique_names


def test_revision_model_preserves_ordered_immutable_snapshot_identity() -> None:
    check_names = _constraint_names(IntelligenceRevision, CheckConstraint)
    unique_names = _constraint_names(IntelligenceRevision, UniqueConstraint)

    assert "ck_intelligence_revision_number" in check_names
    assert "uq_intelligence_item_revision" in unique_names
    assert "uq_intelligence_item_revision_hash" in unique_names
    assert IntelligenceRevision.__table__.c.snapshot.nullable is False


def test_persistence_relationships_are_bidirectional_and_delete_orphans() -> None:
    provenance = IntelligenceItem.provenance.property
    revisions = IntelligenceItem.revisions.property

    assert provenance.back_populates == "item"
    assert revisions.back_populates == "item"
    assert "delete-orphan" in provenance.cascade
    assert "delete-orphan" in revisions.cascade
