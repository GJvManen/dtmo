from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSOLE = ROOT / "backend/dtmo/unified_console.py"


def test_grafana_embeds_use_same_origin_subpath() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    assert "const base='/grafana'" in text
    assert ":3000" not in text
    assert "/grafana/d/dtmo-operations/dtmo-operations" in text or "${base}/d/dtmo-operations/dtmo-operations" in text
    assert "/grafana/d/dtmo-intelligence/dtmo-intelligence" in text or "${base}/d/dtmo-intelligence/dtmo-intelligence" in text


def test_native_fallback_remains_available() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    for marker in (
        "severity-chart",
        "severity-table",
        "source-chart",
        "source-table",
        "connector-chart",
        "connector-table",
    ):
        assert marker in text
