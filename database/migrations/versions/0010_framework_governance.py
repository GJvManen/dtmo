"""Add versioned governance frameworks and explicit intelligence mappings.

Revision ID: 0010_framework_governance
Revises: 0009_managed_rbac_assignments
Create Date: 2026-08-12
"""

from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

revision: str = "0010_framework_governance"
down_revision: str | None = "0009_managed_rbac_assignments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    frameworks = op.create_table(
        "governance_frameworks",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False),
        sa.Column("version_label", sa.String(length=255), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("authority", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("coverage_mode", sa.String(length=32), nullable=False),
        sa.Column("expected_object_count", sa.Integer(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "coverage_mode IN ('mapping', 'context_only')",
            name="ck_governance_framework_coverage_mode",
        ),
    )
    op.create_table(
        "intelligence_framework_mappings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("framework_id", sa.String(length=64), nullable=False),
        sa.Column("framework_version", sa.String(length=64), nullable=False),
        sa.Column("object_type", sa.String(length=32), nullable=False),
        sa.Column("object_id", sa.String(length=128), nullable=False),
        sa.Column("object_title", sa.String(length=500), nullable=True),
        sa.Column("intelligence_id", sa.Uuid(), nullable=False),
        sa.Column("mapping_status", sa.String(length=32), nullable=False),
        sa.Column("provenance_reference", sa.Text(), nullable=False),
        sa.Column("confidence_score", sa.Integer(), nullable=False),
        sa.Column("mapping_reason", sa.Text(), nullable=False),
        sa.Column("review_state", sa.String(length=32), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reviewed_by", sa.String(length=255), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["framework_id"], ["governance_frameworks.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["intelligence_id"], ["intelligence_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "object_type IN ('control', 'technique', 'category', 'scoring_context')",
            name="ck_framework_mapping_object_type",
        ),
        sa.CheckConstraint(
            "mapping_status IN ('mapped', 'context_only')",
            name="ck_framework_mapping_status",
        ),
        sa.CheckConstraint(
            "review_state IN ('pending', 'approved', 'rejected')",
            name="ck_framework_mapping_review_state",
        ),
        sa.CheckConstraint(
            "confidence_score >= 0 AND confidence_score <= 100",
            name="ck_framework_mapping_confidence",
        ),
        sa.UniqueConstraint(
            "framework_id",
            "framework_version",
            "object_type",
            "object_id",
            "intelligence_id",
            name="uq_framework_mapping_target_intelligence",
        ),
    )
    op.create_index("ix_intelligence_framework_mappings_framework_id", "intelligence_framework_mappings", ["framework_id"])
    op.create_index("ix_intelligence_framework_mappings_intelligence_id", "intelligence_framework_mappings", ["intelligence_id"])
    op.create_index("ix_framework_mapping_framework_review", "intelligence_framework_mappings", ["framework_id", "review_state"])
    op.create_index("ix_framework_mapping_object", "intelligence_framework_mappings", ["framework_id", "object_type", "object_id"])

    verified = datetime(2026, 8, 12, tzinfo=UTC)
    op.bulk_insert(
        frameworks,
        [
            {
                "id": "normenkader-ibp",
                "name": "Normenkader IBP",
                "version": "2024-06-06",
                "version_label": "Inhoud ongewijzigd sinds 6 juni 2024",
                "kind": "education-security-and-privacy",
                "authority": "Kennisnet",
                "source_url": "https://normenkaderibp.kennisnet.nl/",
                "coverage_mode": "mapping",
                "expected_object_count": 94,
                "metadata_json": {"information_security_norms": 69, "privacy_norms": 25},
                "last_verified_at": verified,
            },
            {
                "id": "mitre-attack",
                "name": "MITRE ATT&CK",
                "version": "19.1",
                "version_label": "ATT&CK v19.1",
                "kind": "threat-behavior-taxonomy",
                "authority": "MITRE",
                "source_url": "https://attack.mitre.org/resources/versions/",
                "coverage_mode": "mapping",
                "expected_object_count": None,
                "metadata_json": {"mapping_granularity": "technique"},
                "last_verified_at": verified,
            },
            {
                "id": "cvss",
                "name": "CVSS",
                "version": "4.0",
                "version_label": "CVSS v4.0",
                "kind": "vulnerability-scoring-context",
                "authority": "FIRST",
                "source_url": "https://www.first.org/cvss/v4.0/",
                "coverage_mode": "context_only",
                "expected_object_count": None,
                "metadata_json": {"first_class_vector_in_dtmo": False},
                "last_verified_at": verified,
            },
            {
                "id": "nist-csf",
                "name": "NIST Cybersecurity Framework",
                "version": "2.0",
                "version_label": "NIST CSF 2.0",
                "kind": "cybersecurity-risk-framework",
                "authority": "NIST",
                "source_url": "https://www.nist.gov/cyberframework",
                "coverage_mode": "mapping",
                "expected_object_count": None,
                "metadata_json": {"mapping_granularity": "category-or-subcategory"},
                "last_verified_at": verified,
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_framework_mapping_object", table_name="intelligence_framework_mappings")
    op.drop_index("ix_framework_mapping_framework_review", table_name="intelligence_framework_mappings")
    op.drop_index("ix_intelligence_framework_mappings_intelligence_id", table_name="intelligence_framework_mappings")
    op.drop_index("ix_intelligence_framework_mappings_framework_id", table_name="intelligence_framework_mappings")
    op.drop_table("intelligence_framework_mappings")
    op.drop_table("governance_frameworks")
