"""Add purgeable privacy-minimized audit projections.

Revision ID: 0004_privacy_projection
Revises: 0003_persistent_audit
Create Date: 2026-08-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_privacy_projection"
down_revision: str | None = "0003_persistent_audit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "audit_projection_records",
        sa.Column("source_event_id", sa.Uuid(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("principal_reference", sa.String(length=80), nullable=False),
        sa.Column("principal_type", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("resource_reference", sa.String(length=80), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("request_reference", sa.String(length=80), nullable=False),
        sa.Column("source_event_hash", sa.String(length=64), nullable=False),
        sa.Column("retention_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("legal_hold", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("legal_hold_reference", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_event_id"],
            ["audit_event_records.event_id"],
            name="fk_audit_projection_source_event",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("source_event_id"),
        sa.CheckConstraint(
            "(legal_hold = false AND legal_hold_reference IS NULL) OR "
            "(legal_hold = true AND legal_hold_reference IS NOT NULL)",
            name="ck_audit_projection_legal_hold_reference",
        ),
    )
    op.create_index(
        "ix_audit_projection_expiry_hold",
        "audit_projection_records",
        ["retention_expires_at", "legal_hold"],
        unique=False,
    )
    op.create_index(
        "ix_audit_projection_action_occurred",
        "audit_projection_records",
        ["action", "occurred_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_audit_projection_action_occurred", table_name="audit_projection_records")
    op.drop_index("ix_audit_projection_expiry_hold", table_name="audit_projection_records")
    op.drop_table("audit_projection_records")
