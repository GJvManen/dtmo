from __future__ import annotations

from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.config import Settings
from dtmo.integration_readiness import integration_readiness
from dtmo.intelligence.model import IntelligenceSeverity, IntelligenceType
from dtmo.persistence.models import ConnectorRun, IntelligenceItem


_RUNTIME_RUN_IDS: dict[str, str] = {
    "taranis": "taranis",
    "misp": "misp",
    "ail": "ail",
}


def build_integration_capabilities(
    settings: Settings,
    latest_runs: dict[str, ConnectorRun] | None = None,
) -> list[dict[str, Any]]:
    """Describe governed integration capability without inventing runtime health.

    Command Center reuses the canonical Administration readiness model so an
    integration that still needs configuration or explicit activation is always
    presented with an actionable Administration path. Persisted connector
    execution is exposed only as a historical runtime observation, never as a
    health claim.
    """

    latest_runs = latest_runs or {}
    capabilities: list[dict[str, Any]] = []
    for readiness in integration_readiness(settings):
        run_id = _RUNTIME_RUN_IDS.get(readiness.id, "")
        run = latest_runs.get(run_id) if run_id else None
        if readiness.enabled and readiness.activation_blockers:
            state = "configuration-required"
        elif readiness.enabled:
            state = "enabled"
        else:
            state = "configuration-required"
        capabilities.append(
            {
                "id": readiness.id,
                "label": readiness.name,
                "state": state,
                "enabled": readiness.enabled,
                "configured": readiness.configured,
                "credential_configured": readiness.credential_configured,
                "can_activate": readiness.can_activate,
                "activation_blockers": list(readiness.activation_blockers),
                "readiness_state": readiness.state,
                "action": readiness.action,
                "detail": readiness.detail,
                "scheduled_collection": bool(
                    readiness.enabled
                    and run_id
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
    return {
        "intelligence_7d": [],
        "severity_distribution": [],
        "source_distribution": [],
        "type_distribution": [],
    }


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
        severity_counts = {severity.value: 0 for severity in IntelligenceSeverity}
        for severity, count in severity_rows:
            severity_counts[_severity_value(severity)] = int(count or 0)

        source_rows = (
            await session.execute(
                select(IntelligenceItem.source_id, func.count())
                .group_by(IntelligenceItem.source_id)
                .order_by(desc(func.count()), IntelligenceItem.source_id)
            )
        ).all()

        type_rows = (
            await session.execute(
                select(IntelligenceItem.item_type, func.count())
                .group_by(IntelligenceItem.item_type)
            )
        ).all()
        type_counts = {item_type.value: 0 for item_type in IntelligenceType}
        for item_type, count in type_rows:
            type_counts[_severity_value(item_type)] = int(count or 0)

        trends = {
            "intelligence_7d": [
                {"date": day.isoformat(), "count": count}
                for day, count in daily_counts.items()
            ],
            "severity_distribution": [
                {"severity": severity.value, "count": severity_counts.get(severity.value, 0)}
                for severity in IntelligenceSeverity
            ],
            "source_distribution": [
                {"source_id": str(source_id), "count": int(count or 0)}
                for source_id, count in source_rows
            ],
            "type_distribution": [
                {"item_type": item_type.value, "count": type_counts.get(item_type.value, 0)}
                for item_type in IntelligenceType
            ],
        }

        connector_runs = (
            await session.scalars(
                select(ConnectorRun)
                .where(ConnectorRun.connector_id.in_(["taranis", "misp", "ail"]))
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
            "Command Center values and trends are canonical DTMO read models. Integration readiness "
            "reuses the governed Administration contract; capabilities requiring configuration or explicit "
            "activation remain configuration-required in the Command Center so the operator receives an "
            "actionable Administration path. Persisted runtime observations are historical evidence only and "
            "are never labelled healthy. Missing canonical-store evidence is reported as unavailable rather "
            "than synthesized."
        ),
    }
