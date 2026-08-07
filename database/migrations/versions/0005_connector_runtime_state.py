"""Add persistent connector runtime state, health history and quarantine recovery.

Revision ID: 0005_connector_state
Revises: 0004_privacy_projection
Create Date: 2026-08-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_connector_state"
down_revision: str | None = "0004_privacy_projection"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "connector_runtime_states",
        sa.Column("connector_id", sa.String(length=128), nullable=False),
        sa.Column("last_run_id", sa.Uuid(), nullable=True),
        sa.Column("last_success_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_failure_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("consecutive_failures", sa.Integer(), server_default="0", nullable=False),
        sa.Column("circuit_open_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("health_status", sa.String(length=32), server_default="unknown", nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("connector_id"),
        sa.CheckConstraint("consecutive_failures >= 0", name="ck_connector_state_failures_nonnegative"),
        sa.CheckConstraint(
            "health_status IN ('unknown', 'healthy', 'degraded', 'isolated')",
            name="ck_connector_state_health_status",
        ),
    )
    op.create_index("ix_connector_runtime_states_health_status", "connector_runtime_states", ["health_status"])

    op.create_table(
        "connector_health_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("connector_id", sa.String(length=128), nullable=False),
        sa.Column("run_id", sa.Uuid(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("duration_seconds", sa.Float(), server_default="0", nullable=False),
        sa.Column("record_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("quarantine_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_code", sa.String(length=128), nullable=True),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("publish_approved", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.ForeignKeyConstraint(["connector_id"], ["connector_runtime_states.connector_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("connector_id", "run_id", name="uq_connector_health_run"),
        sa.CheckConstraint("status IN ('success', 'failure')", name="ck_connector_health_status"),
        sa.CheckConstraint("duration_seconds >= 0", name="ck_connector_health_duration"),
        sa.CheckConstraint("record_count >= 0", name="ck_connector_health_record_count"),
        sa.CheckConstraint("quarantine_count >= 0", name="ck_connector_health_quarantine_count"),
        sa.CheckConstraint("publish_approved = false", name="ck_connector_health_never_publishes"),
    )
    op.create_index("ix_connector_health_events_connector_id", "connector_health_events", ["connector_id"])
    op.create_index("ix_connector_health_events_run_id", "connector_health_events", ["run_id"])
    op.create_index("ix_connector_health_events_status", "connector_health_events", ["status"])
    op.create_index("ix_connector_health_history", "connector_health_events", ["connector_id", "observed_at"])

    op.create_table(
        "connector_quarantine_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("connector_id", sa.String(length=128), nullable=False),
        sa.Column("run_id", sa.Uuid(), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("reason", sa.String(length=128), nullable=False),
        sa.Column("raw_evidence_hash", sa.String(length=64), nullable=False),
        sa.Column("raw_evidence", sa.JSON(), nullable=False),
        sa.Column("quarantined_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("recovery_status", sa.String(length=32), server_default="pending", nullable=False),
        sa.Column("recovered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("recovered_by", sa.String(length=255), nullable=True),
        sa.Column("review_reference", sa.String(length=255), nullable=True),
        sa.Column("publish_approved", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("connector_id", "run_id", "raw_evidence_hash", name="uq_connector_quarantine_evidence"),
        sa.CheckConstraint(
            "recovery_status IN ('pending', 'released_to_candidate', 'rejected')",
            name="ck_connector_quarantine_recovery_status",
        ),
        sa.CheckConstraint(
            "(recovery_status = 'pending' AND recovered_at IS NULL AND recovered_by IS NULL AND review_reference IS NULL) OR "
            "(recovery_status != 'pending' AND recovered_at IS NOT NULL AND recovered_by IS NOT NULL AND review_reference IS NOT NULL)",
            name="ck_connector_quarantine_recovery_evidence",
        ),
        sa.CheckConstraint("publish_approved = false", name="ck_connector_quarantine_never_publishes"),
    )
    op.create_index("ix_connector_quarantine_records_connector_id", "connector_quarantine_records", ["connector_id"])
    op.create_index("ix_connector_quarantine_records_run_id", "connector_quarantine_records", ["run_id"])
    op.create_index("ix_connector_quarantine_records_reason", "connector_quarantine_records", ["reason"])
    op.create_index("ix_connector_quarantine_records_recovery_status", "connector_quarantine_records", ["recovery_status"])
    op.create_index(
        "ix_connector_quarantine_pending",
        "connector_quarantine_records",
        ["connector_id", "recovery_status", "quarantined_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_connector_quarantine_pending", table_name="connector_quarantine_records")
    op.drop_index("ix_connector_quarantine_records_recovery_status", table_name="connector_quarantine_records")
    op.drop_index("ix_connector_quarantine_records_reason", table_name="connector_quarantine_records")
    op.drop_index("ix_connector_quarantine_records_run_id", table_name="connector_quarantine_records")
    op.drop_index("ix_connector_quarantine_records_connector_id", table_name="connector_quarantine_records")
    op.drop_table("connector_quarantine_records")
    op.drop_index("ix_connector_health_history", table_name="connector_health_events")
    op.drop_index("ix_connector_health_events_status", table_name="connector_health_events")
    op.drop_index("ix_connector_health_events_run_id", table_name="connector_health_events")
    op.drop_index("ix_connector_health_events_connector_id", table_name="connector_health_events")
    op.drop_table("connector_health_events")
    op.drop_index("ix_connector_runtime_states_health_status", table_name="connector_runtime_states")
    op.drop_table("connector_runtime_states")
