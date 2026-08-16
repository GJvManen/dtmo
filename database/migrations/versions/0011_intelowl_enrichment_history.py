"""Add durable governed IntelOwl enrichment history.

Revision ID: 0011_intelowl_enrichment_history
Revises: 0010_framework_governance
Create Date: 2026-08-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011_intelowl_enrichment_history"
down_revision: str | None = "0010_framework_governance"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "intelowl_enrichment_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("job_id", sa.String(length=255), nullable=False),
        sa.Column("observable_type", sa.String(length=64), nullable=False),
        sa.Column("observable_value", sa.Text(), nullable=False),
        sa.Column("handling", sa.String(length=64), nullable=False),
        sa.Column("analyzers", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("partial", sa.Boolean(), nullable=False),
        sa.Column("reports", sa.JSON(), nullable=False),
        sa.Column("raw_result", sa.JSON(), nullable=False),
        sa.Column("requested_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("external_share_authorized", sa.Boolean(), nullable=False),
        sa.Column("local_compromise_proven", sa.Boolean(), nullable=False),
        sa.CheckConstraint(
            "external_share_authorized = false",
            name="ck_intelowl_enrichment_no_share_authority",
        ),
        sa.CheckConstraint(
            "local_compromise_proven = false",
            name="ck_intelowl_enrichment_no_compromise_proof",
        ),
        sa.ForeignKeyConstraint(["item_id"], ["intelligence_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("item_id", "job_id", name="uq_intelowl_enrichment_item_job"),
    )
    op.create_index(
        "ix_intelowl_enrichment_records_item_id",
        "intelowl_enrichment_records",
        ["item_id"],
    )
    op.create_index(
        "ix_intelowl_enrichment_records_status",
        "intelowl_enrichment_records",
        ["status"],
    )
    op.create_index(
        "ix_intelowl_enrichment_records_created_at",
        "intelowl_enrichment_records",
        ["created_at"],
    )
    op.create_index(
        "ix_intelowl_enrichment_item_created",
        "intelowl_enrichment_records",
        ["item_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_intelowl_enrichment_item_created", table_name="intelowl_enrichment_records")
    op.drop_index("ix_intelowl_enrichment_records_created_at", table_name="intelowl_enrichment_records")
    op.drop_index("ix_intelowl_enrichment_records_status", table_name="intelowl_enrichment_records")
    op.drop_index("ix_intelowl_enrichment_records_item_id", table_name="intelowl_enrichment_records")
    op.drop_table("intelowl_enrichment_records")
