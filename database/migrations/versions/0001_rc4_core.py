"""Create RC4 core intelligence tables.

Revision ID: 0001_rc4_core
Revises:
Create Date: 2026-08-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_rc4_core"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "intelligence_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("item_type", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("canonical_url", sa.Text(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("discovered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Integer(), nullable=False),
        sa.Column("education_relevance", sa.Integer(), nullable=False),
        sa.Column("review_status", sa.String(length=32), nullable=False),
        sa.Column("share_approved", sa.Boolean(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "source_id",
            "external_id",
            name="uq_intelligence_source_external",
        ),
    )
    op.create_index(
        "ix_intelligence_items_source_id",
        "intelligence_items",
        ["source_id"],
    )
    op.create_index(
        "ix_intelligence_items_item_type",
        "intelligence_items",
        ["item_type"],
    )
    op.create_index(
        "ix_intelligence_items_content_hash",
        "intelligence_items",
        ["content_hash"],
    )
    op.create_index(
        "ix_intelligence_items_severity",
        "intelligence_items",
        ["severity"],
    )
    op.create_index(
        "ix_intelligence_items_education_relevance",
        "intelligence_items",
        ["education_relevance"],
    )
    op.create_index(
        "ix_intelligence_items_review_status",
        "intelligence_items",
        ["review_status"],
    )
    op.create_index(
        "ix_intelligence_items_share_approved",
        "intelligence_items",
        ["share_approved"],
    )
    op.create_index(
        "ix_intelligence_priority",
        "intelligence_items",
        ["severity", "education_relevance", "review_status"],
    )

    op.create_table(
        "connector_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("connector_id", sa.String(length=128), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("fetched", sa.Integer(), nullable=False),
        sa.Column("inserted", sa.Integer(), nullable=False),
        sa.Column("duplicates", sa.Integer(), nullable=False),
        sa.Column("error_count", sa.Integer(), nullable=False),
        sa.Column("duration_seconds", sa.Float(), nullable=True),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_connector_runs_connector_id",
        "connector_runs",
        ["connector_id"],
    )
    op.create_index("ix_connector_runs_status", "connector_runs", ["status"])

    op.create_table(
        "provenance_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("source_title", sa.String(length=500), nullable=True),
        sa.Column("publisher", sa.String(length=255), nullable=True),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("exact_passage", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["intelligence_items.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_provenance_records_item_id",
        "provenance_records",
        ["item_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_provenance_records_item_id", table_name="provenance_records")
    op.drop_table("provenance_records")
    op.drop_index("ix_connector_runs_status", table_name="connector_runs")
    op.drop_index("ix_connector_runs_connector_id", table_name="connector_runs")
    op.drop_table("connector_runs")
    op.drop_index("ix_intelligence_priority", table_name="intelligence_items")
    op.drop_index("ix_intelligence_items_share_approved", table_name="intelligence_items")
    op.drop_index("ix_intelligence_items_review_status", table_name="intelligence_items")
    op.drop_index(
        "ix_intelligence_items_education_relevance",
        table_name="intelligence_items",
    )
    op.drop_index("ix_intelligence_items_severity", table_name="intelligence_items")
    op.drop_index("ix_intelligence_items_content_hash", table_name="intelligence_items")
    op.drop_index("ix_intelligence_items_item_type", table_name="intelligence_items")
    op.drop_index("ix_intelligence_items_source_id", table_name="intelligence_items")
    op.drop_table("intelligence_items")
