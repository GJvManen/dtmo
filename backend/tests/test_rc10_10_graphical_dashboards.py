from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

import dtmo.dashboards as dashboard_module
from dtmo.dashboards import _group_counts, _seven_day_trend, dashboard_summary, dashboards_page


def test_dashboard_exposes_real_data_visualizations() -> None:
    body = dashboards_page().body.decode("utf-8")

    assert "RC12.2 graphical dashboards" in body
    assert "/api/v1/dashboards/summary" in body
    assert "Intelligence trend — 7 dagen" in body
    assert "intelligence_trend_7d" in body
    assert "Severity-verdeling" in body
    assert "Reviewstatus" in body
    assert "Top intelligencebronnen" in body
    assert "Connector health" in body
    assert "<svg" in body
    assert "Staafdiagram" in body


def test_dashboard_has_accessible_table_alternatives_and_live_status() -> None:
    body = dashboards_page().body.decode("utf-8")

    assert 'role="status"' in body
    assert 'aria-live="polite"' in body
    assert "chart-table" in body
    assert 'scope="col"' in body
    assert 'role="img"' in body
    assert 'aria-label="Staafdiagram"' in body


def test_dashboard_preserves_read_only_governance_boundary() -> None:
    body = dashboards_page().body.decode("utf-8")

    assert "dashboards zijn read-only" in body
    assert "geen review- of publicatiebevoegdheid" in body
    assert "afzonderlijke menselijke goedkeuring" in body
    assert "X-DTMO-Subject" in body
    assert "X-DTMO-Roles" in body
    assert "X-DTMO-API-Key" in body
    assert "localStorage" not in body


def test_group_counts_normalizes_enum_like_values() -> None:
    class EnumLike:
        value = "critical"

    class ExecuteResult:
        def all(self) -> list[tuple[object, int]]:
            return [(EnumLike(), 4), ("high", 2)]

    class Session:
        async def execute(self, _statement: object) -> ExecuteResult:
            return ExecuteResult()

    result = asyncio.run(_group_counts(Session(), dashboard_module.IntelligenceItem.severity))  # type: ignore[arg-type]
    assert result == {"critical": 4, "high": 2}


def test_seven_day_trend_returns_bounded_chronological_buckets() -> None:
    now = datetime.now(UTC)

    class ScalarResult:
        def all(self) -> list[datetime | None]:
            return [now, now - timedelta(days=2), now - timedelta(days=2), None, now - timedelta(days=12)]

    class Session:
        async def scalars(self, _statement: object) -> ScalarResult:
            return ScalarResult()

    trend = asyncio.run(_seven_day_trend(Session()))  # type: ignore[arg-type]
    keys = list(trend)

    assert len(keys) == 7
    assert keys == sorted(keys)
    assert trend[now.date().isoformat()] == 1
    assert trend[(now - timedelta(days=2)).date().isoformat()] == 2
    assert sum(trend.values()) == 3


def test_dashboard_summary_aggregates_current_contract(monkeypatch: Any) -> None:
    class Session:
        def __init__(self) -> None:
            self.values = iter([12, 3, 78.44])

        async def scalar(self, _statement: object) -> int | float:
            return next(self.values)

    grouped = iter(
        [
            {"critical": 2, "high": 3},
            {"pending": 4, "approved": 8},
            {"nvd": 7, "cisa-kev": 5},
            {"healthy": 9, "degraded": 1},
        ]
    )

    async def fake_group_counts(_session: object, _column: object) -> dict[str, int]:
        return next(grouped)

    async def fake_trend(_session: object) -> dict[str, int]:
        return {"2026-08-05": 1, "2026-08-06": 2}

    monkeypatch.setattr(dashboard_module, "_group_counts", fake_group_counts)
    monkeypatch.setattr(dashboard_module, "_seven_day_trend", fake_trend)

    result = asyncio.run(dashboard_summary(object(), Session()))  # type: ignore[arg-type]

    assert result["total_intelligence"] == 12
    assert result["new_last_24h"] == 3
    assert result["average_confidence"] == 78.4
    assert result["severity"] == {"critical": 2, "high": 3}
    assert result["review_status"] == {"pending": 4, "approved": 8}
    assert result["sources"] == {"nvd": 7, "cisa-kev": 5}
    assert result["connector_health"] == {"healthy": 9, "degraded": 1}
    assert result["intelligence_trend_7d"] == {"2026-08-05": 1, "2026-08-06": 2}
    assert result["publication_boundary"] == "human-review-and-separate-share-approval-required"
    assert isinstance(result["generated_at"], str)
