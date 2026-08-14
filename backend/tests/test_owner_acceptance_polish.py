from __future__ import annotations

from fastapi.testclient import TestClient

from dtmo.governance_crosswalk_experience import _SCRIPT
from dtmo.main import app


def test_canonical_console_loads_augmented_framework_script() -> None:
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    assert 'src="/ui/framework-experience.js"' in page.text

    script = client.get("/ui/framework-experience.js")
    assert script.status_code == 200
    assert "governance-crosswalk" in script.text
    assert "/api/v1/governance/control-crosswalk" in script.text
    assert "Owner-acceptance contrast repair" in script.text


def test_crosswalk_script_repairs_recent_intelligence_contrast() -> None:
    assert ".card.severity-card{color:var(--text)!important}" in _SCRIPT
    assert ".card.severity-card .intel-meta>span:not(.severity-pill){color:#d7e3f1!important}" in _SCRIPT
    assert ".card.severity-card p{color:var(--text)!important}" in _SCRIPT
    assert ".card.severity-card a{color:#9bd3ff!important" in _SCRIPT


def test_crosswalk_is_inserted_when_higher_composition_layer_omits_it() -> None:
    assert "function ensurePanel()" in _SCRIPT
    assert "framework.insertAdjacentHTML('afterend', panelMarkup)" in _SCRIPT
    assert "panel.dataset.crosswalkInitialized" in _SCRIPT
