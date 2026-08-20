"""Add durable Cortex analyzer execution history.

Revision ID: 0015_cortex_analysis_history
Revises: 0014_thehive_handoff_state
Create Date: 2026-08-20
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0015_cortex_analysis_history"
down_revision: str | None = "0014_thehive_handoff_state"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "cortex_analysis_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.String(length=255), nullable=False),
        sa.Column("observable_type", sa.String(length=64), nullable=False),
        sa.Column("observable_value", sa.Text(), nullable=False),
        sa.Column("analyzer_id", sa.String(length=255), nullable=False),
        sa.Column("tlp", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("report", sa.JSON(), nullable=False),
        sa.Column("raw_result", sa.JSON(), nullable=False),
        sa.Column("requested_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("external_share_authorized", sa.Boolean(), nullable=False),
        sa.Column("local_compromise_proven", sa.Boolean(), nullable=False),
        sa.CheckConstraint("tlp >= 0 AND tlp <= 3", name="ck_cortex_analysis_tlp"),
        sa.CheckConstraint("external_share_authorized = false", name="ck_cortex_analysis_no_share_authority"),
        sa.CheckConstraint("local_compromise_proven = false", name="ck_cortex_analysis_no_compromise_proof"),
        sa.ForeignKeyConstraint(["item_id"], ["intelligence_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("item_id", "job_id", name="uq_cortex_analysis_item_job"),
    )
    op.create_index("ix_cortex_analysis_records_item_id", "cortex_analysis_records", ["item_id"])
    op.create_index("ix_cortex_analysis_records_status", "cortex_analysis_records", ["status"])
    op.create_index("ix_cortex_analysis_records_created_at", "cortex_analysis_records", ["created_at"])
    op.create_index("ix_cortex_analysis_item_created", "cortex_analysis_records", ["item_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_cortex_analysis_item_created", table_name="cortex_analysis_records")
    op.drop_index("ix_cortex_analysis_records_created_at", table_name="cortex_analysis_records")
    op.drop_index("ix_cortex_analysis_records_status", table_name="cortex_analysis_records")
    op.drop_index("ix_cortex_analysis_records_item_id", table_name="cortex_analysis_records")
    op.drop_table("cortex_analysis_records")
