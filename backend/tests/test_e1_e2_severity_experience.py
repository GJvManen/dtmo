from __future__ import annotations

import pytest
from fastapi import HTTPException

from dtmo.intelligence.model import IntelligenceSeverity
from dtmo.severity_experience import _PAGE, _SCRIPT, _selected_severities, router


def test_default_severity_filter_uses_complete_canonical_enum() -> None:
    selected = _selected_severities(None)
    assert selected == tuple(IntelligenceSeverity)
    assert [item.value for item in selected] == [
        "informational",
        "low",
        "medium",
        "high",
        "critical",
    ]


def test_severity_filter_deduplicates_and_rejects_unknown_values() -> None:
    selected = _selected_severities(["HIGH", "low", "high"])
    assert selected == (IntelligenceSeverity.HIGH, IntelligenceSeverity.LOW)

    with pytest.raises(HTTPException) as exc_info:
        _selected_severities(["urgent"])
    assert exc_info.value.status_code == 400
    assert "unsupported severity filter" in str(exc_info.value.detail)


def test_console_contains_shared_overview_and_intelligence_filters() -> None:
    assert _PAGE.count('data-severity-filter role="group"') == 2
    for severity in ("informational", "low", "medium", "high", "critical"):
        assert f'value="{severity}"' in _PAGE
        assert f"severity-{severity}" in _PAGE
    assert "Severityfilter" in _PAGE
    assert "severity-dot" in _PAGE
    assert "data-severity-filter-status" in _PAGE


def test_console_uses_requested_classification_labels_and_colours() -> None:
    for label in ("Informatief", "Laag", "Middel", "Hoog", "Kritiek"):
        assert label in _PAGE
    assert ".severity-informational{--severity-color:#667085" in _PAGE
    assert ".severity-low{--severity-color:#16803c" in _PAGE
    assert ".severity-medium{--severity-color:#c2410c" in _PAGE
    assert ".severity-high{--severity-color:#b42318" in _PAGE


def test_severity_experience_preserves_rc13_administration_and_governance() -> None:
    assert 'data-view-panel="administration"' in _PAGE
    assert 'id="rbac-administration"' in _PAGE
    assert 'data-view-panel="governance"' in _PAGE
    assert 'id="governance-knowledge"' in _PAGE
    assert '/ui/rc13-governance.js' in _PAGE
    assert '/ui/severity-experience.js' in _PAGE


def test_severity_script_composes_overview_recent_and_search_filtering() -> None:
    assert "/api/v1/console/severity-summary" in _SCRIPT
    assert "/api/v1/console/recent-intelligence?limit=100" in _SCRIPT
    assert "/api/v1/intelligence/search?q=" in _SCRIPT
    assert "event.stopImmediatePropagation()" in _SCRIPT
    assert "selected.size" in _SCRIPT
    assert "Minimaal één severity moet geselecteerd blijven." in _SCRIPT
    assert "Geen intelligence binnen dit severityfilter." in _SCRIPT
    assert "Nog geen intelligence ingested." in _SCRIPT
    assert "severity-pill" in _SCRIPT
    assert "severity-bar" in _SCRIPT


def test_severity_router_exposes_canonical_console_roots() -> None:
    canonical_routes = [
        route
        for route in router.routes
        if route.path in {"/", "/ui/console"}
    ]
    assert {route.path for route in canonical_routes} == {"/", "/ui/console"}
    assert all(
        route.endpoint.__module__ == "dtmo.severity_experience"
        for route in canonical_routes
    )


def test_severity_colours_are_supplemented_by_text_and_structure() -> None:
    # Colour is deliberately supplementary: every choice/pill also contains the
    # severity text and the chart/table keeps explicit labels/counts.
    assert "do not encode severity by colour alone" not in _PAGE.lower()
    for label in ("Informatief", "Laag", "Middel", "Hoog", "Kritiek"):
        assert label in _PAGE
    assert "<th>Severity</th><th>Aantal</th>" in _SCRIPT
    assert "aria-hidden=\"true\" class=\"severity-dot\"" in _SCRIPT
