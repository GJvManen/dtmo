from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/UnifiedIntelligenceWorkspace.tsx"


def test_threat_intelligence_opens_with_canonical_recent_discovery():
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "useEffect" in text
    assert "'/api/v1/command-center'" in text
    assert "Recent canonical intelligence" in text
    assert "Run an enabled governed source from Sources & Collection" in text
    assert "Select a recent item or search hit" in text


def test_default_discovery_preserves_evidence_boundaries():
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "populated only from objects already present in canonical DTMO persistence" in text
    assert "never converted into synthetic intelligence" in text
    assert "Neither path grants review, publication, sharing, connector-execution or case-mutation authority" in text


def test_ioc_route_does_not_fake_inventory_during_threat_intelligence_slice():
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "IOC inventory is the next recovery slice" in text
    assert "does not fabricate an IOC inventory from arbitrary text" in text
