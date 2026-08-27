from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2] / "frontend/src/VisualAnalyticsWorkspace.tsx"


def test_visual_analytics_component_is_read_only_and_fail_closed():
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "credentials: 'same-origin'" in text
    assert "No attributable data is available for this view." in text
    assert "No attributable values are synthesized." in text
    assert "does not prove live connectivity" in text
    assert "does not prove local exposure" in text
    assert "does not grant review, sharing or publication authority" in text
    for forbidden in ("method: 'POST'", 'method: "POST"', "method: 'PUT'", "method: 'DELETE'"):
        assert forbidden not in text
