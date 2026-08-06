"""Add privacy-minimized audit projection storage.

Revision ID: 0004_minimized_projection
Revises: 0003_persistent_audit
Create Date: 2026-08-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_minimized_projection"
down_revision: str | None = "0003_persistent_audit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "minimized_audit_projection_records",
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("principal_reference", sa.String(length=96), nullable=False),
        sa.Column("principal_type", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("resource_reference", sa.String(length=96), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("request_reference", sa.String(length=96), nullable=False),
        sa.Column("source_event_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("legal_hold", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("event_id"),
        sa.UniqueConstraint("source_event_hash", name="uq_minimized_projection_source_hash"),
    )
    op.create_index(
        "ix_minimized_projection_expires_hold",
        "minimized_audit_projection_records",
        ["expires_at", "legal_hold"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_minimized_projection_expires_hold",
        table_name="minimized_audit_projection_records",
    )
    op.drop_table("minimized_audit_projection_records")
