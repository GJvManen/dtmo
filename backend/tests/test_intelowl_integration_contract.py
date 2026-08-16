from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md"
ROADMAP = ROOT / "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md"
CURRENT_STATE = ROOT / "docs/project/CURRENT_STATE.md"
README = ROOT / "README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_intelowl_contract_records_upstream_and_bounded_api_surface() -> None:
    text = _read(CONTRACT)
    required = (
        "v6.7.0",
        "/api/analyze_observable",
        "/api/jobs/{job_id}",
        "API-token authentication",
        "CVE",
        "IP address",
        "domain",
        "URL",
        "cryptographic hash",
    )
    for marker in required:
        assert marker in text, f"missing IntelOwl contract marker: {marker}"


def test_intelowl_contract_preserves_least_privilege_and_share_authority() -> None:
    text = _read(CONTRACT)
    required = (
        "must not be an IntelOwl superuser",
        "MUST NOT invoke every available IntelOwl analyzer by default",
        "explicit allowlist",
        "Email and other personally identifying generic observables are **excluded by default**",
        "No IntelOwl job success",
        "human approval and governed MISP/export controls remain authoritative",
        "IntelOwl MISP/OpenCTI/Slack/email/abuse-submission connectors are outside this initial path",
    )
    for marker in required:
        assert marker in text, f"missing IntelOwl authority marker: {marker}"


def test_intelowl_contract_is_fail_closed_and_provenance_first() -> None:
    text = _read(CONTRACT)
    required = (
        "Missing or unknown TLP/handling data fails closed",
        "upstream job ID",
        "analyzer/playbook name",
        "raw result/evidence reference",
        "429",
        "partial job success",
        "must not make unrelated DTMO read paths unavailable",
        "MUST NOT be represented as proof",
    )
    for marker in required:
        assert marker in text, f"missing IntelOwl fail-closed/provenance marker: {marker}"


def test_intelowl_contract_preserves_service_and_licensing_boundary() -> None:
    text = _read(CONTRACT)
    required = (
        "AGPL-3.0",
        "separate service/API consumer",
        "does not vendor IntelOwl or pyIntelOwl source",
        "explicit licensing review",
        "does not authorize source redistribution",
    )
    for marker in required:
        assert marker in text, f"missing IntelOwl licensing marker: {marker}"


def test_phase11_authoritative_status_moves_to_intelowl() -> None:
    contract = _read(CONTRACT)
    roadmap = _read(ROADMAP)
    current_state = _read(CURRENT_STATE)
    readme = _read(README)

    assert "PHASE 11.3 CONTRACT BASELINE" in contract
    assert "11.2 Taranis → DTMO canonical adapter" in roadmap
    assert "REPOSITORY_COMPLETE" in roadmap
    assert "11.3 IntelOwl enrichment integration" in roadmap
    assert "CONTRACT BASELINE IN EXACT-HEAD VALIDATION" in roadmap
    assert "Phase 11.3 IntelOwl" in current_state
    assert "Phase 11.3 IntelOwl" in readme
    assert "not production authorized" in current_state
    assert "not production authorized" in readme
