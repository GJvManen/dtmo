from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md"
INTEGRATION = ROOT / "docs/integrations/OPENCTI_INTEGRATION.md"
RUNBOOK = ROOT / "docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md"
QA_GATE = ROOT / "docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md"
ROADMAP = ROOT / "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md"
CURRENT_STATE = ROOT / "docs/project/CURRENT_STATE.md"
README = ROOT / "README.md"
PORTAL = ROOT / "docs/README.md"
SECURITY = ROOT / "docs/security/SECURITY_OVERVIEW.md"
EVIDENCE = ROOT / "docs/evidence/EVIDENCE_INDEX.md"
ADAPTER = ROOT / "backend/dtmo/integrations/opencti.py"
ADAPTER_TESTS = ROOT / "backend/tests/test_phase11_4_opencti_adapter.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_opencti_contract_records_upstream_api_data_and_license_boundary() -> None:
    text = _read(CONTRACT)
    required = (
        "OpenCTI 7.260811.0", "GraphQL API", "STIX 2.1", "TAXII 2.1",
        "Access-controlled OpenCTI streams", "Apache License 2.0",
        "OpenCTI Enterprise Edition License", "separate service/API consumer",
        "does not vendor OpenCTI source",
    )
    for marker in required:
        assert marker in text, f"missing OpenCTI contract marker: {marker}"


def test_opencti_contract_preserves_identity_markings_provenance_and_authority() -> None:
    text = _read(CONTRACT)
    required = (
        "DTMO canonical UUID", "STIX 2.1 `id`", "markings/TLP/PAP context", "confidence",
        "never synthesize an OpenCTI identity from mutable labels or names",
        "No OpenCTI query, import, stream event, relationship, confidence value, connector result or successful mutation grants DTMO publication/share authority",
        "Human approval and governed DTMO export/MISP controls remain authoritative",
        "Graph presence does not prove local exposure, exploitability, compromise",
    )
    for marker in required:
        assert marker in text, f"missing OpenCTI identity/authority marker: {marker}"


def test_opencti_contract_is_least_privilege_and_fail_closed() -> None:
    text = _read(CONTRACT)
    required = (
        "dedicated non-human OpenCTI identity", "no `Bypass all capabilities`", "runtime secrets",
        "`401` and `403` fail closed", "missing, malformed or unknown marking/TLP context fails closed",
        "partial pages or interrupted stream windows do not advance a checkpoint",
        "must not make unrelated DTMO read paths unavailable", "MISP synchronization", "create TheHive cases",
    )
    for marker in required:
        assert marker in text, f"missing OpenCTI fail-closed marker: {marker}"


def test_phase11_status_preserves_completed_opencti_and_misp_boundaries() -> None:
    roadmap = _read(ROADMAP)
    current_state = _read(CURRENT_STATE)
    readme = _read(README)
    portal = _read(PORTAL)
    assert "11.3 IntelOwl enrichment integration" in roadmap
    assert "11.4 OpenCTI knowledge-graph integration" in roadmap
    assert "11.5 MISP consolidation" in roadmap
    assert "11.6 TheHive incident/case handoff" in roadmap
    for text in (roadmap, current_state, readme, portal):
        assert "PASS / REPOSITORY_COMPLETE" in text
    for text in (current_state, portal):
        assert "Phase 11.4 OpenCTI" in text
        assert "Phase 11.5 MISP" in text
    for text in (current_state, readme, portal):
        assert "not production authorized" in text


def test_opencti_adapter_and_professional_documentation_are_exposed() -> None:
    portal = _read(PORTAL)
    for path in (
        "architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md", "integrations/OPENCTI_INTEGRATION.md",
        "operations/OPENCTI_INTEGRATION_RUNBOOK.md", "qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md",
    ):
        assert path in portal
    integration = _read(INTEGRATION)
    for marker in (
        "backend/dtmo/integrations/opencti.py", "commit_page(page)",
        "external_share_authorized=false", "local_compromise_proven=false", "DTMO_FEATURE_OPENCTI_READ",
    ):
        assert marker in integration
    assert "OpenCTI" in _read(SECURITY)
    assert "OpenCTI" in _read(EVIDENCE)
    assert ADAPTER.exists() and ADAPTER_TESTS.exists() and RUNBOOK.exists() and QA_GATE.exists()
