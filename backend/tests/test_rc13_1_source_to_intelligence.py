from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from dtmo.auth.policy import Principal, Role
from dtmo.unified_console import recent_console_intelligence, unified_console_root


class _ScalarResult:
    def __init__(self, rows: list[object]) -> None:
        self._rows = rows

    def all(self) -> list[object]:
        return self._rows


class _FakeSession:
    def __init__(self, rows: list[object]) -> None:
        self._rows = rows

    async def scalars(self, _statement: object) -> _ScalarResult:
        return _ScalarResult(self._rows)


@pytest.mark.asyncio
async def test_recent_intelligence_uses_canonical_database_projection() -> None:
    discovered = datetime(2026, 8, 11, 14, 0, tzinfo=UTC)
    row = SimpleNamespace(
        id="11111111-1111-1111-1111-111111111111",
        source_id="nvd-cve",
        title="Synthetic NVD advisory",
        summary="Canonical database fixture",
        severity=SimpleNamespace(value="high"),
        confidence_score=90,
        education_relevance=85,
        review_status="candidate",
        share_approved=False,
        canonical_url="https://example.invalid/CVE-TEST",
        published_at=None,
        discovered_at=discovered,
    )
    principal = Principal(subject="alice", roles=frozenset({Role.ANALYST}))

    result = await recent_console_intelligence(
        principal=principal,
        session=_FakeSession([row]),  # type: ignore[arg-type]
        limit=20,
    )

    assert result == [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "source_id": "nvd-cve",
            "title": "Synthetic NVD advisory",
            "summary": "Canonical database fixture",
            "severity": "high",
            "confidence_score": 90,
            "education_relevance": 85,
            "review_status": "candidate",
            "share_approved": False,
            "canonical_url": "https://example.invalid/CVE-TEST",
            "published_at": None,
            "discovered_at": discovered.isoformat(),
        }
    ]


def test_console_exposes_functional_source_to_intelligence_journey() -> None:
    body = unified_console_root().body.decode("utf-8")

    assert "Eén applicatieshell. Legacy `/ui/*`-views" not in body
    assert "/api/v1/console/recent-intelligence?limit=20" in body
    assert "Built-in · handmatige run beschikbaar" in body
    assert "Frameworkbronnen registreren" in body
    assert "Feed laden en verwerken" in body
    assert "loadRecentIntelligence()" in body
    assert "overview-trend-chart" in body
    assert "overview-severity-chart" in body
    assert "overview-connector-chart" in body
    assert "Native DTMO-analytics tonen alleen meetbare data" in body
    assert "Geen data om te visualiseren" in body
    assert "Geen intelligence data · bronstatus geladen" in body


def test_grafana_is_not_required_for_initial_console_render() -> None:
    body = unified_console_root().body.decode("utf-8")

    assert "Advanced Grafana dashboards" in body
    assert "Grafana blijft een afzonderlijk geauthenticeerde operations-view" in body
    startup = body.split("const initial=", 1)[1]
    assert "initGrafana();" not in startup
