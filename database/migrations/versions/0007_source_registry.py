"""Add governed source registry.

Revision ID: 0007_source_registry
Revises: 0006_connector_replay
Create Date: 2026-08-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_source_registry"
down_revision: str | None = "0006_connector_replay"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "source_definitions",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("endpoint_url", sa.String(length=2048), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("interval_seconds", sa.Integer(), server_default="3600", nullable=False),
        sa.Column("reliability", sa.String(length=32), server_default="medium", nullable=False),
        sa.Column("secret_ref", sa.String(length=512), nullable=True),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("interval_seconds >= 60 AND interval_seconds <= 86400", name="ck_source_interval"),
        sa.CheckConstraint("source_type IN ('cisa-kev', 'json-feed')", name="ck_source_type"),
        sa.CheckConstraint("reliability IN ('authoritative', 'high', 'medium', 'low')", name="ck_source_reliability"),
    )
    op.create_index("ix_source_definitions_source_type", "source_definitions", ["source_type"])
    op.create_index("ix_source_definitions_enabled", "source_definitions", ["enabled"])


def downgrade() -> None:
    op.drop_index("ix_source_definitions_enabled", table_name="source_definitions")
    op.drop_index("ix_source_definitions_source_type", table_name="source_definitions")
    op.drop_table("source_definitions")
