"""Add durable OpenCTI canonical mapping and immutable reconciliation history.

Revision ID: 0012_opencti_mapping_persistence
Revises: 0011_intelowl_enrichment_history
Create Date: 2026-08-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012_opencti_mapping_persistence"
down_revision: str | None = "0011_intelowl_enrichment_history"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "opencti_object_mappings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("opencti_id", sa.String(length=255), nullable=False),
        sa.Column("stix_id", sa.String(length=255), nullable=False),
        sa.Column("entity_type", sa.String(length=128), nullable=False),
        sa.Column("parent_types", sa.JSON(), nullable=False),
        sa.Column("markings", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Integer(), nullable=True),
        sa.Column("upstream_created_at", sa.String(length=64), nullable=True),
        sa.Column("upstream_updated_at", sa.String(length=64), nullable=True),
        sa.Column("external_references", sa.JSON(), nullable=False),
        sa.Column("provenance", sa.JSON(), nullable=False),
        sa.Column("snapshot_hash", sa.String(length=64), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("external_share_authorized", sa.Boolean(), nullable=False),
        sa.Column("local_compromise_proven", sa.Boolean(), nullable=False),
        sa.CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 100)", name="ck_opencti_mapping_confidence"),
        sa.CheckConstraint("external_share_authorized = false", name="ck_opencti_mapping_no_share_authority"),
        sa.CheckConstraint("local_compromise_proven = false", name="ck_opencti_mapping_no_compromise_proof"),
        sa.ForeignKeyConstraint(["item_id"], ["intelligence_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("item_id", "opencti_id", name="uq_opencti_mapping_item_opencti"),
        sa.UniqueConstraint("item_id", "stix_id", name="uq_opencti_mapping_item_stix"),
    )
    op.create_index("ix_opencti_object_mappings_item_id", "opencti_object_mappings", ["item_id"])
    op.create_index("ix_opencti_object_mappings_entity_type", "opencti_object_mappings", ["entity_type"])
    op.create_index("ix_opencti_object_mappings_last_seen_at", "opencti_object_mappings", ["last_seen_at"])
    op.create_index("ix_opencti_mapping_item_seen", "opencti_object_mappings", ["item_id", "last_seen_at"])

    op.create_table(
        "opencti_mapping_revisions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("mapping_id", sa.Uuid(), nullable=False),
        sa.Column("snapshot_hash", sa.String(length=64), nullable=False),
        sa.Column("snapshot", sa.JSON(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["mapping_id"], ["opencti_object_mappings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("mapping_id", "snapshot_hash", name="uq_opencti_mapping_revision_hash"),
    )
    op.create_index("ix_opencti_mapping_revisions_mapping_id", "opencti_mapping_revisions", ["mapping_id"])
    op.create_index("ix_opencti_mapping_revisions_recorded_at", "opencti_mapping_revisions", ["recorded_at"])


def downgrade() -> None:
    op.drop_index("ix_opencti_mapping_revisions_recorded_at", table_name="opencti_mapping_revisions")
    op.drop_index("ix_opencti_mapping_revisions_mapping_id", table_name="opencti_mapping_revisions")
    op.drop_table("opencti_mapping_revisions")
    op.drop_index("ix_opencti_mapping_item_seen", table_name="opencti_object_mappings")
    op.drop_index("ix_opencti_object_mappings_last_seen_at", table_name="opencti_object_mappings")
    op.drop_index("ix_opencti_object_mappings_entity_type", table_name="opencti_object_mappings")
    op.drop_index("ix_opencti_object_mappings_item_id", table_name="opencti_object_mappings")
    op.drop_table("opencti_object_mappings")
