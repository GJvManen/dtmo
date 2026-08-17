"""Add durable TheHive case handoff reservation and reconciliation state.

Revision ID: 0014_thehive_handoff_state
Revises: 0013_misp_synchronization_state
Create Date: 2026-08-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0014_thehive_handoff_state"
down_revision: str | None = "0013_misp_synchronization_state"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "thehive_handoff_state",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("request_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("requested_by", sa.String(length=255), nullable=False),
        sa.Column("organization", sa.String(length=255), nullable=False),
        sa.Column("tlp", sa.String(length=32), nullable=False),
        sa.Column("pap", sa.String(length=32), nullable=False),
        sa.Column("authority_snapshot", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("thehive_case_id", sa.String(length=255), nullable=True),
        sa.Column("thehive_case_number", sa.String(length=64), nullable=True),
        sa.Column("outcome", sa.JSON(), nullable=False),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("external_share_authorized", sa.Boolean(), nullable=False),
        sa.Column("local_compromise_proven", sa.Boolean(), nullable=False),
        sa.CheckConstraint("status IN ('reserved','delivered','ambiguous','failed')", name="ck_thehive_handoff_status"),
        sa.CheckConstraint("external_share_authorized = false", name="ck_thehive_handoff_no_share_authority"),
        sa.CheckConstraint("local_compromise_proven = false", name="ck_thehive_handoff_no_compromise_proof"),
        sa.ForeignKeyConstraint(["item_id"], ["intelligence_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("request_id", name="uq_thehive_handoff_request"),
        sa.UniqueConstraint("thehive_case_id", name="uq_thehive_handoff_case"),
    )
    op.create_index("ix_thehive_handoff_state_item_id", "thehive_handoff_state", ["item_id"])
    op.create_index("ix_thehive_handoff_state_status", "thehive_handoff_state", ["status"])
    op.create_index("ix_thehive_handoff_item_created", "thehive_handoff_state", ["item_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_thehive_handoff_item_created", table_name="thehive_handoff_state")
    op.drop_index("ix_thehive_handoff_state_status", table_name="thehive_handoff_state")
    op.drop_index("ix_thehive_handoff_state_item_id", table_name="thehive_handoff_state")
    op.drop_table("thehive_handoff_state")
