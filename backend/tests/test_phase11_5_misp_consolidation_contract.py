from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md"
QA_GATE = ROOT / "docs/qa/PHASE11_5_MISP_CONSOLIDATION_CONTRACT_GATE.md"
READ_INTEGRATION = ROOT / "docs/integrations/MISP_READ_INTEGRATION.md"
EXPORT_DOC = ROOT / "docs/intelligence/MISP_GOVERNED_EXPORT.md"
READ_CONNECTOR = ROOT / "backend/dtmo/connectors/misp.py"
EXPORT_API = ROOT / "backend/dtmo/misp_export_api.py"
EXPORT_GOVERNANCE = ROOT / "backend/dtmo/governance/misp_export.py"
ROADMAP = ROOT / "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md"
CURRENT_STATE = ROOT / "docs/project/CURRENT_STATE.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_misp_contract_records_upstream_service_api_and_license_boundary() -> None:
    text = _read(CONTRACT)
    required = (
        "MISP v2.5.44",
        "GNU AGPL-3.0",
        "separate service/API consumer",
        "does not vendor, fork, embed, or redistribute MISP core source",
        "POST /events/restSearch",
        "POST /events/add",
    )
    for marker in required:
        assert marker in text, f"missing MISP contract marker: {marker}"


def test_misp_contract_preserves_identity_restrictions_and_human_authority() -> None:
    text = _read(CONTRACT)
    required = (
        "MISP event UUID is the stable upstream identity",
        "distribution, sharing-group and TLP/tag restrictions",
        "never sets DTMO `share_approved`",
        "Service accounts, connectors, schedulers, IntelOwl, OpenCTI and MISP itself cannot grant DTMO share approval",
        "cannot be broadened on re-export",
        "created **unpublished**",
        "blocks automated replay until an operator reconciles",
    )
    for marker in required:
        assert marker in text, f"missing MISP authority marker: {marker}"


def test_misp_contract_excludes_implicit_federation_and_false_evidence() -> None:
    text = _read(CONTRACT)
    required = (
        "does **not** enable MISP server push/pull synchronization",
        "OpenCTI↔MISP synchronization is likewise excluded",
        "Authentication/authorization failures (`401`/`403`) fail closed",
        "does **not** prove live MISP credentials",
        "TheHive case creation",
        "Cortex adoption",
    )
    for marker in required:
        assert marker in text, f"missing MISP fail-closed/exclusion marker: {marker}"


def test_existing_misp_paths_are_present_for_consolidation() -> None:
    assert READ_CONNECTOR.exists()
    assert EXPORT_API.exists()
    assert EXPORT_GOVERNANCE.exists()
    assert READ_INTEGRATION.exists()
    assert EXPORT_DOC.exists()
    assert QA_GATE.exists()

    assert "events/restSearch" in _read(READ_CONNECTOR)
    assert "events/add" in _read(EXPORT_GOVERNANCE)
    assert "Permission.SHARE_APPROVE" in _read(EXPORT_API)
    assert "service accounts cannot export intelligence to MISP" in _read(EXPORT_GOVERNANCE)


def test_phase11_status_moves_to_misp_contract_validation() -> None:
    roadmap = _read(ROADMAP)
    state = _read(CURRENT_STATE)
    assert "11.4 OpenCTI" in roadmap
    assert "PASS / REPOSITORY_COMPLETE" in roadmap
    assert "11.5 MISP consolidation" in roadmap
    assert "CONTRACT IN EXACT-HEAD VALIDATION" in roadmap
    assert "Phase 11.4" in state
    assert "PASS / REPOSITORY_COMPLETE" in state
    assert "Phase 11.5 MISP" in state
    assert "not production authorized" in state
