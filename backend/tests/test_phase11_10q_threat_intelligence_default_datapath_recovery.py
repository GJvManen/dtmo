from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POPULATION = ROOT / "frontend/src/ThreatIntelligencePopulation.tsx"
DOC = ROOT / "docs/qa/THREAT_INTELLIGENCE_DEFAULT_DATAPATH_RECOVERY.md"


def test_threat_intelligence_population_reads_builtin_runtime_readiness():
    text = POPULATION.read_text(encoding="utf-8")
    for marker in (
        "'/api/v1/source-center/status'",
        "supported-built-in",
        "manual_run_available",
        "Load ${source.name} now",
        "`/connectors/${encodeURIComponent(source.id)}/run`",
        "'/api/v1/admin/sources'",
        "`/api/v1/admin/sources/${encodeURIComponent(source.id)}/run`",
    ):
        assert marker in text


def test_threat_intelligence_population_preserves_governed_execution_boundaries():
    text = POPULATION.read_text(encoding="utf-8")
    assert "manage:connectors" in text
    assert "server-authorized source paths" in text
    assert "does not prove exploitation, local compromise, review approval, publication or external sharing authority" in text
    assert "feature_live_connectors" not in text


def test_default_datapath_recovery_documentation_keeps_acceptance_boundary():
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "clean supported installation",
        "CISA KEV",
        "Threat Intelligence",
        "IOC Explorer",
        "not production-equivalent evidence",
        "not owner functional acceptance",
    ):
        assert marker in text
