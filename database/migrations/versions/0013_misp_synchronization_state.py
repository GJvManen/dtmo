"""Add durable MISP synchronization state and authority envelope.

Revision ID: 0013_misp_synchronization_state
Revises: 0012_opencti_mapping_persistence
Create Date: 2026-08-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0013_misp_synchronization_state"
down_revision: str | None = "0012_opencti_mapping_persistence"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "misp_synchronization_state",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("event_uuid", sa.String(length=64), nullable=False),
        sa.Column("event_timestamp", sa.String(length=64), nullable=True),
        sa.Column("distribution", sa.String(length=1), nullable=False),
        sa.Column("sharing_group_id", sa.String(length=64), nullable=True),
        sa.Column("tlp_tags", sa.JSON(), nullable=False),
        sa.Column("authority_snapshot", sa.JSON(), nullable=False),
        sa.Column("snapshot_hash", sa.String(length=64), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("external_share_authorized", sa.Boolean(), nullable=False),
        sa.CheckConstraint("distribution IN ('0','1','2','3','4','5')", name="ck_misp_sync_distribution"),
        sa.CheckConstraint(
            "(distribution = '4' AND sharing_group_id IS NOT NULL) OR distribution <> '4'",
            name="ck_misp_sync_sharing_group_required",
        ),
        sa.CheckConstraint("external_share_authorized = false", name="ck_misp_sync_no_share_authority"),
        sa.ForeignKeyConstraint(["item_id"], ["intelligence_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("item_id"),
        sa.UniqueConstraint("event_uuid"),
        sa.UniqueConstraint("event_uuid", "snapshot_hash", name="uq_misp_sync_event_snapshot"),
    )


def downgrade() -> None:
    op.drop_table("misp_synchronization_state")
