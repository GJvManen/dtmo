from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md"
ROADMAP = ROOT / "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md"
ASSESSMENT = ROOT / "docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_taranis_contract_records_read_only_api_surface() -> None:
    text = _read(CONTRACT)
    required = (
        "/api/auth/method",
        "/api/auth/login",
        "/api/auth/refresh",
        "/api/assess/osint-sources-list",
        "/api/assess/news-items",
        "/api/assess/news-items/{item_id}",
        "/api/assess/news-items/{item_id}/cti",
        "/api/assess/stories",
        "/api/assess/stories/{story_id}",
        "/api/assess/stories/{story_id}/cti",
        "ASSESS_ACCESS",
    )
    for marker in required:
        assert marker in text, f"missing Taranis contract marker: {marker}"


def test_taranis_contract_is_fail_closed_for_authority_and_markings() -> None:
    text = _read(CONTRACT)
    required = (
        "MUST NOT require `ASSESS_CREATE`, `ASSESS_UPDATE`, `ASSESS_DELETE`",
        "MUST NOT receive or exercise",
        "never becomes DTMO share approval",
        "Classification transformation is fail-closed",
        "unknown/unmapped values fail closed",
        "403` is an authorization/configuration failure",
    )
    for marker in required:
        assert marker in text, f"missing fail-closed contract marker: {marker}"


def test_taranis_contract_requires_idempotency_provenance_and_failure_isolation() -> None:
    text = _read(CONTRACT)
    required = (
        "taranis:source:{upstream_source_id}",
        "taranis:news-item:{upstream_item_id}",
        "taranis:story:{upstream_story_id}",
        "A replay of an unchanged upstream object MUST be idempotent",
        "Each canonical record created or updated through this adapter must be able to answer",
        "The connector is fail-isolated",
        "partial page failure",
        "do not advance checkpoint past uncommitted records",
    )
    for marker in required:
        assert marker in text, f"missing durability/provenance marker: {marker}"


def test_taranis_contract_preserves_phase_boundaries() -> None:
    contract = _read(CONTRACT)
    roadmap = _read(ROADMAP)
    assessment = _read(ASSESSMENT)

    assert "Phase 11.2" in contract
    assert "PROCEED TO 11.2 AFTER EXACT-HEAD ACCEPTANCE" in contract
    assert "11.2 Taranis → DTMO canonical adapter" in roadmap
    assert "Taranis → DTMO canonical adapter contract" in assessment
    assert "No Taranis implementation source is copied" in contract
    assert "not a deployment, staging, external-assurance or production authorization decision" in contract
