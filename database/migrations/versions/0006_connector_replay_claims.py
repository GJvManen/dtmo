"""Add persistent connector replay claims.

Revision ID: 0006_connector_replay
Revises: 0005_connector_state
Create Date: 2026-08-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_connector_replay"
down_revision: str | None = "0005_connector_state"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "connector_replay_claims",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("connector_id", sa.String(length=128), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=False),
        sa.Column("payload_digest", sa.String(length=64), nullable=False),
        sa.Column("first_run_id", sa.Uuid(), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_uri", sa.String(length=2048), nullable=False),
        sa.Column("publish_approved", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("connector_id", "external_id", "payload_digest", name="uq_connector_replay_claim"),
        sa.CheckConstraint("publish_approved = false", name="ck_connector_replay_never_publishes"),
    )
    op.create_index("ix_connector_replay_claims_connector_id", "connector_replay_claims", ["connector_id"])
    op.create_index("ix_connector_replay_claims_external_id", "connector_replay_claims", ["external_id"])
    op.create_index("ix_connector_replay_claims_first_run_id", "connector_replay_claims", ["first_run_id"])


def downgrade() -> None:
    op.drop_index("ix_connector_replay_claims_first_run_id", table_name="connector_replay_claims")
    op.drop_index("ix_connector_replay_claims_external_id", table_name="connector_replay_claims")
    op.drop_index("ix_connector_replay_claims_connector_id", table_name="connector_replay_claims")
    op.drop_table("connector_replay_claims")
