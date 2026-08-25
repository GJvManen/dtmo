from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "frontend/src/App.tsx"
UX = ROOT / "docs/ux/OBJECT_CONTEXT_DEFAULT_BEHAVIOR.md"


def test_object_context_is_closed_on_initial_workbench_load() -> None:
    app = APP.read_text(encoding="utf-8")
    assert "const [contextOpen, setContextOpen] = useState(false);" in app
    assert "const [contextOpen, setContextOpen] = useState(true);" not in app


def test_object_context_remains_explicitly_user_toggleable() -> None:
    app = APP.read_text(encoding="utf-8")
    assert "onClick={() => setContextOpen((value) => !value)}" in app
    assert 'aria-expanded={contextOpen}' in app
    assert "<ContextRail open={contextOpen}" in app


def test_object_context_default_behavior_is_documented() -> None:
    text = UX.read_text(encoding="utf-8")
    assert "closed by default" in text
    assert "explicit user action" in text
    assert "does not change server-side authorization" in text
