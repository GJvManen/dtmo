"""Add persistent append-only audit-chain storage.

Revision ID: 0003_persistent_audit
Revises: 0002_rc5_canonical
Create Date: 2026-08-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_persistent_audit"
down_revision: str | None = "0002_rc5_canonical"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "audit_event_records",
        sa.Column("sequence_number", sa.BigInteger(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("principal", sa.String(length=255), nullable=False),
        sa.Column("principal_type", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("resource", sa.Text(), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("request_id", sa.String(length=255), nullable=False),
        sa.Column("provenance_reference", sa.Text(), nullable=True),
        sa.Column("previous_hash", sa.String(length=64), nullable=False),
        sa.Column("event_hash", sa.String(length=64), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("sequence_number"),
        sa.UniqueConstraint("event_id", name="uq_audit_event_id"),
        sa.UniqueConstraint("event_hash", name="uq_audit_event_hash"),
        sa.UniqueConstraint(
            "sequence_number", "previous_hash", name="uq_audit_sequence_previous_hash"
        ),
    )
    op.create_index(
        "ix_audit_event_occurred_at", "audit_event_records", ["occurred_at"], unique=False
    )
    op.create_index(
        "ix_audit_event_principal_action",
        "audit_event_records",
        ["principal", "action"],
        unique=False,
    )
    op.execute(
        """
        CREATE FUNCTION reject_audit_event_mutation() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'audit_event_records is append-only';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER audit_event_records_append_only
        BEFORE UPDATE OR DELETE ON audit_event_records
        FOR EACH ROW EXECUTE FUNCTION reject_audit_event_mutation();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS audit_event_records_append_only ON audit_event_records")
    op.execute("DROP FUNCTION IF EXISTS reject_audit_event_mutation()")
    op.drop_index("ix_audit_event_principal_action", table_name="audit_event_records")
    op.drop_index("ix_audit_event_occurred_at", table_name="audit_event_records")
    op.drop_table("audit_event_records")
