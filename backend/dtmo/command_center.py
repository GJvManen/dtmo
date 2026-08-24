from __future__ import annotations

from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.config import Settings
from dtmo.intelligence.model import IntelligenceSeverity
from dtmo.persistence.models import ConnectorRun, IntelligenceItem


_INTEGRATIONS: tuple[dict[str, str], ...] = (
    {"id": "taranis", "label": "Taranis", "flag": "feature_taranis_connector", "api_base": "taranis_api_base", "run_id": "taranis"},
    {"id": "intelowl", "label": "IntelOwl", "flag": "feature_intelowl_enrichment", "api_base": "intelowl_api_base", "run_id": ""},
    {"id": "opencti", "label": "OpenCTI", "flag": "feature_opencti_read", "api_base": "opencti_api_base", "run_id": ""},
    {"id": "misp", "label": "MISP", "flag": "feature_misp_connector", "api_base": "misp_api_base", "run_id": "misp"},
    {"id": "thehive", "label": "TheHive", "flag": "feature_thehive_handoff", "api_base": "thehive_api_base", "run_id": ""},
    {"id": "cortex", "label": "Cortex", "flag": "feature_cortex_analysis", "api_base": "cortex_api_base", "run_id": ""},
)


def build_integration_capabilities(
    settings: Settings,
    latest_runs: dict[str, ConnectorRun] | None = None,
) -> list[dict[str, Any]]:
    """Describe governed integration capability without inventing runtime health.

    Configuration or a feature flag is not proof that an upstream service is
    reachable or healthy. Only persisted connector execution state is exposed as
    runtime observation in this Phase 11.10c read model.
    """

    latest_runs = latest_runs or {}
    capabilities: list[dict[str, Any]] = []
    for definition in _INTEGRATIONS:
        enabled = bool(getattr(settings, definition["flag"]))
        api_base = str(getattr(settings, definition["api_base"])).strip()
        configured = bool(api_base)
        run = latest_runs.get(definition["run_id"]) if definition["run_id"] else None
        if enabled and not configured:
            state = "configuration-required"
        elif enabled:
            state = "enabled"
        else:
            state = "disabled"
        capabilities.append(
            {
                "id": definition["id"],
                "label": definition["label"],
                "state": state,
                "enabled": enabled,
                "configured": configured,
                "scheduled_collection": bool(
                    enabled
                    and definition["run_id"]
                    and settings.feature_live_connectors
                ),
                "runtime_observation": run.status if run is not None else None,
                "last_observed_at": (
                    (run.finished_at or run.started_at).astimezone(UTC).isoformat()
                    if run is not None
                    else None
                ),
                "runtime_health_claim": False,
            }
        )
    return capabilities


def _metric(metric_id: str, label: str, value: int | None, tone: str) -> dict[str, Any]:
    return {"id": metric_id, "label": label, "value": value, "tone": tone}


def _severity_value(value: object) -> str:
    return str(getattr(value, "value", value))


def _empty_trends() -> dict[str, list[dict[str, Any]]]:
    return {"intelligence_7d": [], "severity_distribution": []}


async def build_command_center_snapshot(
    session: AsyncSession,
    settings: Settings,
) -> dict[str, Any]:
    """Build one attributable, read-only Command Center snapshot."""

    now = datetime.now(UTC)
    latest_runs: dict[str, ConnectorRun] = {}
    data_state = "available"
    recent_intelligence: list[dict[str, Any]] = []
    trends = _empty_trends()
    metrics = [
        _metric("intelligence-total", "Intelligence objects", None, "neutral"),
        _metric("high-priority", "High / critical", None, "critical"),
        _metric("new-24h", "New in 24h", None, "accent"),
        _metric("pending-review", "Pending review", None, "warning"),
        _metric("share-approvals", "Share approvals", None, "warning"),
        _metric("education-relevant", "Education relevance ≥80", None, "accent"),
    ]

    try:
        total = int(await session.scalar(select(func.count()).select_from(IntelligenceItem)) or 0)
        high_priority = int(
            await session.scalar(
                select(func.count())
                .select_from(IntelligenceItem)
                .where(
                    IntelligenceItem.severity.in_(
                        [IntelligenceSeverity.HIGH, IntelligenceSeverity.CRITICAL]
                    )
                )
            )
            or 0
        )
        recent_24h = int(
            await session.scalar(
                select(func.count())
                .select_from(IntelligenceItem)
                .where(IntelligenceItem.discovered_at >= now - timedelta(hours=24))
            )
            or 0
        )
        pending_review = int(
            await session.scalar(
                select(func.count())
                .select_from(IntelligenceItem)
                .where(IntelligenceItem.review_status == "candidate")
            )
            or 0
        )
        share_approvals = int(
            await session.scalar(
                select(func.count())
                .select_from(IntelligenceItem)
                .where(
                    IntelligenceItem.review_status == "reviewed",
                    IntelligenceItem.share_approved.is_(False),
                )
            )
            or 0
        )
        education_relevant = int(
            await session.scalar(
                select(func.count())
                .select_from(IntelligenceItem)
                .where(IntelligenceItem.education_relevance >= 80)
            )
            or 0
        )
        metrics = [
            _metric("intelligence-total", "Intelligence objects", total, "neutral"),
            _metric("high-priority", "High / critical", high_priority, "critical"),
            _metric("new-24h", "New in 24h", recent_24h, "accent"),
            _metric("pending-review", "Pending review", pending_review, "warning"),
            _metric("share-approvals", "Share approvals", share_approvals, "warning"),
            _metric("education-relevant", "Education relevance ≥80", education_relevant, "accent"),
        ]

        items = (
            await session.scalars(
                select(IntelligenceItem)
                .order_by(desc(IntelligenceItem.discovered_at))
                .limit(6)
            )
        ).all()
        recent_intelligence = [
            {
                "id": str(item.id),
                "title": item.title,
                "source_id": item.source_id,
                "severity": _severity_value(item.severity),
                "education_relevance": item.education_relevance,
                "review_status": item.review_status,
                "discovered_at": item.discovered_at.astimezone(UTC).isoformat(),
            }
            for item in items
        ]

        seven_day_start = (now - timedelta(days=6)).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        daily_counts = {
            (seven_day_start + timedelta(days=offset)).date(): 0
            for offset in range(7)
        }
        trend_rows = (
            await session.execute(
                select(IntelligenceItem.discovered_at)
                .where(IntelligenceItem.discovered_at >= seven_day_start)
            )
        ).all()
        for row in trend_rows:
            discovered_at = row[0]
            day = discovered_at.astimezone(UTC).date()
            if day in daily_counts:
                daily_counts[day] += 1

        severity_rows = (
            await session.execute(
                select(IntelligenceItem.severity, func.count())
                .group_by(IntelligenceItem.severity)
            )
        ).all()
        severity_counts = {
            severity.value: 0
            for severity in IntelligenceSeverity
        }
        for severity, count in severity_rows:
            severity_counts[_severity_value(severity)] = int(count or 0)

        trends = {
            "intelligence_7d": [
                {"date": day.isoformat(), "count": count}
                for day, count in daily_counts.items()
            ],
            "severity_distribution": [
                {"severity": severity.value, "count": severity_counts.get(severity.value, 0)}
                for severity in IntelligenceSeverity
            ],
        }

        connector_runs = (
            await session.scalars(
                select(ConnectorRun)
                .where(ConnectorRun.connector_id.in_(["taranis", "misp"]))
                .order_by(desc(ConnectorRun.started_at))
            )
        ).all()
        for run in connector_runs:
            latest_runs.setdefault(run.connector_id, run)
    except Exception:
        data_state = "unavailable"
        trends = _empty_trends()
        with suppress(Exception):
            await session.rollback()

    return {
        "generated_at": now.isoformat(),
        "data_state": data_state,
        "metrics": metrics,
        "recent_intelligence": recent_intelligence,
        "trends": trends,
        "integrations": build_integration_capabilities(settings, latest_runs),
        "evidence_boundary": (
            "Command Center values and trends are canonical DTMO read models. Enabled or configured "
            "integrations are not labelled healthy without runtime observation, and missing "
            "canonical-store evidence is reported as unavailable rather than synthesized."
        ),
    }
