"""Add governed managed principals and role assignments.

Revision ID: 0009_managed_rbac_assignments
Revises: 0008_grafana_reporting_views
Create Date: 2026-08-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009_managed_rbac_assignments"
down_revision: str | None = "0008_grafana_reporting_views"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "managed_principals",
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("principal_type", sa.String(length=32), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("subject"),
        sa.CheckConstraint(
            "principal_type IN ('human', 'service_account')",
            name="ck_managed_principal_type",
        ),
    )
    op.create_index(
        "ix_managed_principals_principal_type",
        "managed_principals",
        ["principal_type"],
    )
    op.create_index(
        "ix_managed_principals_active",
        "managed_principals",
        ["active"],
    )
    op.create_table(
        "managed_role_assignments",
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False),
        sa.Column("assigned_by", sa.String(length=255), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject"],
            ["managed_principals.subject"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("subject", "role"),
    )
    op.create_index(
        "ix_managed_role_assignments_role",
        "managed_role_assignments",
        ["role"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_managed_role_assignments_role",
        table_name="managed_role_assignments",
    )
    op.drop_table("managed_role_assignments")
    op.drop_index("ix_managed_principals_active", table_name="managed_principals")
    op.drop_index(
        "ix_managed_principals_principal_type",
        table_name="managed_principals",
    )
    op.drop_table("managed_principals")
