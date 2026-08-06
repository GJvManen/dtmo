"""Migrate RC4 intelligence data to the RC5 canonical foundation.

Revision ID: 0002_rc5_canonical
Revises: 0001_rc4_core
Create Date: 2026-08-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_rc5_canonical"
down_revision: str | None = "0001_rc4_core"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add canonical confidence, provenance and immutable revision structures."""

    op.add_column(
        "intelligence_items",
        sa.Column("confidence_score", sa.Integer(), nullable=True),
    )
    op.add_column(
        "intelligence_items",
        sa.Column("confidence_level", sa.String(length=32), nullable=True),
    )
    op.add_column(
        "intelligence_items",
        sa.Column("confidence_rationale", sa.JSON(), nullable=True),
    )

    op.execute(
        sa.text(
            """
            UPDATE intelligence_items
            SET confidence_score = LEAST(GREATEST(confidence, 0), 100),
                confidence_level = CASE
                    WHEN confidence >= 90 THEN 'very_high'
                    WHEN confidence >= 75 THEN 'high'
                    WHEN confidence >= 50 THEN 'medium'
                    ELSE 'low'
                END,
                confidence_rationale = CAST('["migrated from RC4 confidence"]' AS JSON)
            """
        )
    )
    op.alter_column("intelligence_items", "confidence_score", nullable=False)
    op.alter_column("intelligence_items", "confidence_level", nullable=False)
    op.alter_column("intelligence_items", "confidence_rationale", nullable=False)
    op.create_check_constraint(
        "ck_intelligence_confidence_score",
        "intelligence_items",
        "confidence_score >= 0 AND confidence_score <= 100",
    )
    op.create_check_constraint(
        "ck_intelligence_education_relevance",
        "intelligence_items",
        "education_relevance >= 0 AND education_relevance <= 100",
    )
    op.create_index(
        "ix_intelligence_items_confidence_level",
        "intelligence_items",
        ["confidence_level"],
    )
    op.drop_column("intelligence_items", "confidence")

    op.add_column(
        "provenance_records",
        sa.Column("source_reliability", sa.String(length=32), nullable=True),
    )
    op.add_column(
        "provenance_records",
        sa.Column("is_primary_source", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "provenance_records",
        sa.Column("content_integrity_verified", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "provenance_records",
        sa.Column("confidence_score", sa.Integer(), nullable=True),
    )
    op.execute(
        sa.text(
            """
            UPDATE provenance_records
            SET source_reliability = 'unknown',
                is_primary_source = FALSE,
                content_integrity_verified = FALSE,
                confidence_score = LEAST(GREATEST(confidence, 0), 100)
            """
        )
    )
    op.alter_column("provenance_records", "source_reliability", nullable=False)
    op.alter_column("provenance_records", "is_primary_source", nullable=False)
    op.alter_column("provenance_records", "content_integrity_verified", nullable=False)
    op.alter_column("provenance_records", "confidence_score", nullable=False)
    op.create_check_constraint(
        "ck_provenance_confidence_score",
        "provenance_records",
        "confidence_score >= 0 AND confidence_score <= 100",
    )
    op.create_unique_constraint(
        "uq_provenance_item_source_content",
        "provenance_records",
        ["item_id", "source_url", "content_hash"],
    )
    op.create_index(
        "ix_provenance_records_source_reliability",
        "provenance_records",
        ["source_reliability"],
    )
    op.drop_column("provenance_records", "confidence")

    op.create_table(
        "intelligence_revisions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("revision_number", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("snapshot", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["intelligence_items.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "revision_number >= 1",
            name="ck_intelligence_revision_number",
        ),
        sa.UniqueConstraint(
            "item_id",
            "revision_number",
            name="uq_intelligence_item_revision",
        ),
        sa.UniqueConstraint(
            "item_id",
            "content_hash",
            name="uq_intelligence_item_revision_hash",
        ),
    )
    op.create_index(
        "ix_intelligence_revisions_item_id",
        "intelligence_revisions",
        ["item_id"],
    )
    op.create_index(
        "ix_intelligence_revisions_content_hash",
        "intelligence_revisions",
        ["content_hash"],
    )


def downgrade() -> None:
    """Restore the RC4 schema while retaining representable confidence values."""

    op.drop_index("ix_intelligence_revisions_content_hash", table_name="intelligence_revisions")
    op.drop_index("ix_intelligence_revisions_item_id", table_name="intelligence_revisions")
    op.drop_table("intelligence_revisions")

    op.add_column(
        "provenance_records",
        sa.Column("confidence", sa.Integer(), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE provenance_records SET confidence = confidence_score"
        )
    )
    op.alter_column("provenance_records", "confidence", nullable=False)
    op.drop_index(
        "ix_provenance_records_source_reliability",
        table_name="provenance_records",
    )
    op.drop_constraint(
        "uq_provenance_item_source_content",
        "provenance_records",
        type_="unique",
    )
    op.drop_constraint(
        "ck_provenance_confidence_score",
        "provenance_records",
        type_="check",
    )
    op.drop_column("provenance_records", "confidence_score")
    op.drop_column("provenance_records", "content_integrity_verified")
    op.drop_column("provenance_records", "is_primary_source")
    op.drop_column("provenance_records", "source_reliability")

    op.add_column(
        "intelligence_items",
        sa.Column("confidence", sa.Integer(), nullable=True),
    )
    op.execute(sa.text("UPDATE intelligence_items SET confidence = confidence_score"))
    op.alter_column("intelligence_items", "confidence", nullable=False)
    op.drop_index(
        "ix_intelligence_items_confidence_level",
        table_name="intelligence_items",
    )
    op.drop_constraint(
        "ck_intelligence_education_relevance",
        "intelligence_items",
        type_="check",
    )
    op.drop_constraint(
        "ck_intelligence_confidence_score",
        "intelligence_items",
        type_="check",
    )
    op.drop_column("intelligence_items", "confidence_rationale")
    op.drop_column("intelligence_items", "confidence_level")
    op.drop_column("intelligence_items", "confidence_score")
