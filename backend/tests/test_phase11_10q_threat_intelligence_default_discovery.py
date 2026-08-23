from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/UnifiedIntelligenceWorkspace.tsx"
IOC_WORKSPACE = ROOT / "frontend/src/IocExplorerWorkspace.tsx"


def test_threat_intelligence_opens_with_canonical_recent_discovery():
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "useEffect" in text
    assert "'/api/v1/command-center'" in text
    assert "Recent canonical intelligence" in text
    assert "Run an enabled governed source from Sources &amp; Collection" in text
    assert "Select a recent item or search hit" in text


def test_default_discovery_preserves_evidence_boundaries():
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "populated only from objects already present in canonical DTMO persistence" in text
    assert "never converted into synthetic intelligence" in text
    assert "Neither path grants review, publication, sharing, connector-execution or case-mutation authority" in text


def test_ioc_route_uses_dedicated_persisted_inventory_without_fabrication():
    intelligence_text = WORKSPACE.read_text(encoding="utf-8")
    ioc_text = IOC_WORKSPACE.read_text(encoding="utf-8")
    assert "if (isIoc) return <IocExplorerWorkspace />" in intelligence_text
    assert "'/api/v1/iocs?size=500'" in ioc_text
    assert "Canonical IOC inventory" in ioc_text
    assert "No text-derived or synthetic IOCs" in ioc_text
    assert "Indicator presence is enrichment evidence, not a maliciousness verdict" in ioc_text
