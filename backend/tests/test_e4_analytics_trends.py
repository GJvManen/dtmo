from __future__ import annotations

from datetime import UTC, datetime, timedelta

from dtmo.analytics_experience import (
    _PAGE,
    _SCRIPT,
    _build_trend_payload,
    _trend_change_percent,
    router,
)
from dtmo.intelligence.model import IntelligenceSeverity


def test_trend_change_percent_handles_zero_baseline_without_inventing_percentage() -> None:
    assert _trend_change_percent(0, 0) == 0.0
    assert _trend_change_percent(3, 0) is None
    assert _trend_change_percent(20, 10) == 100.0
    assert _trend_change_percent(5, 10) == -50.0


def test_24h_trend_separates_volume_change_from_elevated_severity_share() -> None:
    now = datetime(2026, 8, 12, 20, 0, tzinfo=UTC)
    observations = [
        (now - timedelta(hours=1), IntelligenceSeverity.HIGH),
        (now - timedelta(hours=2), IntelligenceSeverity.MEDIUM),
        (now - timedelta(hours=25), IntelligenceSeverity.LOW),
    ]
    payload = _build_trend_payload(
        observations,
        tuple(IntelligenceSeverity),
        "24h",
        now,
    )

    assert payload["window"] == "24h"
    assert len(payload["buckets"]) == 24
    comparison = payload["comparison"]
    assert comparison["current_total"] == 2
    assert comparison["previous_total"] == 1
    assert comparison["volume_delta"] == 1
    assert comparison["volume_change_percent"] == 100.0
    assert comparison["current_elevated_share_percent"] == 50.0
    assert comparison["previous_elevated_share_percent"] == 0.0
    assert comparison["elevated_share_delta_percentage_points"] == 50.0


def test_trend_payload_respects_selected_severity_filter() -> None:
    now = datetime(2026, 8, 12, 20, 0, tzinfo=UTC)
    payload = _build_trend_payload(
        [
            (now - timedelta(hours=1), IntelligenceSeverity.HIGH),
            (now - timedelta(hours=2), IntelligenceSeverity.LOW),
        ],
        (IntelligenceSeverity.LOW,),
        "24h",
        now,
    )
    comparison = payload["comparison"]
    assert comparison["current_total"] == 1
    assert comparison["current_elevated"] == 0
    assert payload["selected_severities"] == ["low"]


def test_7d_and_30d_windows_have_expected_bucket_counts() -> None:
    now = datetime(2026, 8, 12, 20, 0, tzinfo=UTC)
    selected = tuple(IntelligenceSeverity)
    assert len(_build_trend_payload([], selected, "7d", now)["buckets"]) == 7
    assert len(_build_trend_payload([], selected, "30d", now)["buckets"]) == 30


def test_canonical_console_exposes_selectable_trends_in_overview_and_analytics() -> None:
    assert 'data-trend-surface="overview"' in _PAGE
    assert 'data-trend-surface="analytics"' in _PAGE
    assert _PAGE.count('data-trend-window="24h"') == 2
    assert _PAGE.count('data-trend-window="7d"') == 2
    assert _PAGE.count('data-trend-window="30d"') == 2
    assert "Volumestijging" in _PAGE or "volumestijging" in _PAGE
    assert "hoog/kritiek" in _PAGE
    assert "/ui/analytics-experience.js" in _PAGE


def test_trend_script_composes_with_shared_severity_filter() -> None:
    assert "/api/v1/console/trends?window=" in _SCRIPT
    assert "selectedSeverityQuery" in _SCRIPT
    assert "data-severity-filter" in _SCRIPT
    assert "volume_change_percent" in _SCRIPT
    assert "elevated_share_delta_percentage_points" in _SCRIPT
    assert "Informatief" in _SCRIPT
    assert "Middel" in _SCRIPT
    assert "Hoog" in _SCRIPT


def test_trend_enrichment_failure_is_local_and_does_not_poison_global_status() -> None:
    assert "renderTrendUnavailable" in _SCRIPT
    assert "Trenddata tijdelijk niet beschikbaar" in _SCRIPT
    assert "Trend laden mislukt" not in _SCRIPT
    assert "global-status" not in _SCRIPT


def test_analytics_router_owns_canonical_console_roots() -> None:
    routes = [route for route in router.routes if route.path in {"/", "/ui/console"}]
    assert {route.path for route in routes} == {"/", "/ui/console"}
    assert all(route.endpoint.__module__ == "dtmo.analytics_experience" for route in routes)
