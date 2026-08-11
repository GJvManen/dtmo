"""Add least-privilege Grafana reporting views.

Revision ID: 0008_grafana_reporting_views
Revises: 0007_source_registry
Create Date: 2026-08-11
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0008_grafana_reporting_views"
down_revision: str | None = "0007_source_registry"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA dtmo_reporting")
    op.execute(
        """
        CREATE VIEW dtmo_reporting.intelligence_items_safe AS
        SELECT
            discovered_at,
            source_id,
            severity,
            review_status,
            confidence_score,
            education_relevance
        FROM public.intelligence_items
        """
    )
    op.execute(
        """
        CREATE VIEW dtmo_reporting.connector_health_safe AS
        SELECT
            connector_id,
            last_success_at,
            last_failure_at,
            consecutive_failures,
            health_status,
            updated_at
        FROM public.connector_runtime_states
        """
    )


def downgrade() -> None:
    op.execute("DROP VIEW dtmo_reporting.connector_health_safe")
    op.execute("DROP VIEW dtmo_reporting.intelligence_items_safe")
    op.execute("DROP SCHEMA dtmo_reporting")
