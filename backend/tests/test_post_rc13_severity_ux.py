from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

from sqlalchemy import func, select

import dtmo.post_rc13_severity as severity_module
from dtmo.intelligence.model import IntelligenceSeverity
from dtmo.persistence.models import IntelligenceItem
from dtmo.post_rc13_severity import (
    SEVERITY_VALUES,
    _CSS,
    _PAGE,
    _apply_severity,
    filtered_dashboard_summary,
    filtered_recent_console_intelligence,
)
from dtmo.post_rc13_severity_assets import _SCRIPT


def test_shared_severity_contract_exposes_all_canonical_values() -> None:
    assert SEVERITY_VALUES == (
        "informational",
        "low",
        "medium",
        "high",
        "critical",
    )


def test_canonical_postgres_queries_apply_one_shared_severity_predicate() -> None:
    unfiltered = _apply_severity(select(func.count(IntelligenceItem.id)), None)
    filtered = _apply_severity(
        select(func.count(IntelligenceItem.id)), IntelligenceSeverity.HIGH
    )

    assert " WHERE " not in str(unfiltered).upper()
    assert "WHERE intelligence_items.severity =" in str(filtered)


def test_dashboard_summary_keeps_intelligence_aggregates_consistent_and_connector_health_operational(
    monkeypatch: Any,
) -> None:
    class Session:
        def __init__(self) -> None:
            self.values = iter([4, 2, 84.25])

        async def scalar(self, _statement: object) -> int | float:
            return next(self.values)

    seen: list[tuple[str, IntelligenceSeverity | None]] = []

    async def fake_group_counts(
        _session: object,
        column: object,
        severity: IntelligenceSeverity | None,
    ) -> dict[str, int]:
        if column is IntelligenceItem.severity:
            seen.append(("severity", severity))
            return {"high": 4}
        if column is IntelligenceItem.review_status:
            seen.append(("review", severity))
            return {"pending": 3, "reviewed": 1}
        seen.append(("source", severity))
        return {"nvd-cve": 4}

    async def fake_connector_health(_session: object) -> dict[str, int]:
        return {"healthy": 7, "degraded": 1}

    async def fake_trend(
        _session: object, severity: IntelligenceSeverity | None
    ) -> dict[str, int]:
        seen.append(("trend", severity))
        return {"2026-08-12": 4}

    monkeypatch.setattr(severity_module, "_intelligence_group_counts", fake_group_counts)
    monkeypatch.setattr(severity_module, "_connector_health_counts", fake_connector_health)
    monkeypatch.setattr(severity_module, "_filtered_seven_day_trend", fake_trend)

    result = asyncio.run(
        filtered_dashboard_summary(object(), Session(), IntelligenceSeverity.HIGH)  # type: ignore[arg-type]
    )

    assert result["severity_filter"] == "high"
    assert result["severity_values"] == list(SEVERITY_VALUES)
    assert result["total_intelligence"] == 4
    assert result["new_last_24h"] == 2
    assert result["average_confidence"] == 84.2
    assert result["severity"] == {"high": 4}
    assert result["review_status"] == {"pending": 3, "reviewed": 1}
    assert result["sources"] == {"nvd-cve": 4}
    assert result["intelligence_trend_7d"] == {"2026-08-12": 4}
    assert result["connector_health"] == {"healthy": 7, "degraded": 1}
    assert result["connector_health_filter_scope"] == "operational-unfiltered"
    assert result["publication_boundary"] == "human-review-and-separate-share-approval-required"
    assert all(value is IntelligenceSeverity.HIGH for _, value in seen)


def test_recent_intelligence_uses_same_typed_severity_predicate() -> None:
    captured: list[object] = []
    now = datetime.now(UTC)
    item = SimpleNamespace(
        id="00000000-0000-0000-0000-000000000001",
        source_id="nvd-cve",
        title="High severity item",
        summary="Canonical high severity record",
        severity=IntelligenceSeverity.HIGH,
        confidence_score=90,
        education_relevance=75,
        review_status="pending",
        share_approved=False,
        canonical_url="https://example.invalid/CVE-TEST",
        published_at=now,
        discovered_at=now,
    )

    class ScalarResult:
        def all(self) -> list[object]:
            return [item]

    class Session:
        async def scalars(self, statement: object) -> ScalarResult:
            captured.append(statement)
            return ScalarResult()

    rows = asyncio.run(
        filtered_recent_console_intelligence(  # type: ignore[arg-type]
            object(), Session(), 20, IntelligenceSeverity.HIGH
        )
    )

    assert len(rows) == 1
    assert rows[0]["severity"] == "high"
    assert rows[0]["source_id"] == "nvd-cve"
    assert "WHERE intelligence_items.severity =" in str(captured[0])


def test_console_contains_synchronized_overview_and_intelligence_filters() -> None:
    assert 'id="overview-severity-filter"' in _PAGE
    assert 'id="intelligence-severity-filter"' in _PAGE
    assert _PAGE.count("data-severity-filter") >= 2
    for value, label in (
        ("informational", "Informational"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ):
        assert f'<option value="{value}">{label}</option>' in _PAGE
        assert f"severity-{value}" in _PAGE

    assert "/ui/post-rc13-severity.css" in _PAGE
    assert "/ui/post-rc13-severity.js" in _PAGE
    assert 'id="governance-knowledge"' in _PAGE
    assert 'id="rbac-administration"' in _PAGE


def test_severity_semantics_are_accessible_and_not_colour_only() -> None:
    for value in SEVERITY_VALUES:
        assert f".severity-{value}" in _CSS
        assert f"severity-{value}" in _SCRIPT
    assert "aria-label=\"Severity" in _SCRIPT
    assert "severityLabel(value)" in _SCRIPT
    for label in ("Informational", "Low", "Medium", "High", "Critical"):
        assert label in _PAGE
    assert ".severity-critical" in _CSS
    assert "#651426" in _CSS


def test_shared_filter_composes_with_existing_search_and_recent_paths() -> None:
    for path in (
        "/api/v1/dashboards/summary",
        "/api/v1/console/recent-intelligence",
        "/api/v1/intelligence/search",
    ):
        assert path in _SCRIPT
    assert "parsed.searchParams.set('severity', selected)" in _SCRIPT
    assert "sessionStorage.getItem('dtmo.severityFilter')" in _SCRIPT
    assert "localStorage" not in _SCRIPT
    assert "Frameworkmapping blijft afzonderlijk en wordt niet afgeleid uit severity" in _PAGE


def test_default_all_filter_must_not_replace_rc13_truthful_initial_status() -> None:
    # A new browser session defaults to `all`. In that state the accepted RC13
    # refresh/empty-state lifecycle remains authoritative; only a persisted
    # non-default filter triggers an automatic filtered refresh after load.
    assert "if (selected !== 'all') void applySeverity(selected);" in _SCRIPT
    assert "syncControls();\n  void applySeverity(selected);" not in _SCRIPT
