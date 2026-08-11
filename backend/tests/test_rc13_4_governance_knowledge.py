from __future__ import annotations

from pathlib import Path

from dtmo.governance_knowledge import governance_snapshot
from dtmo.rc13_governance import _PAGE


def _framework(snapshot: dict[str, object], framework_id: str) -> dict[str, object]:
    frameworks = snapshot["frameworks"]
    assert isinstance(frameworks, list)
    return next(item for item in frameworks if item["id"] == framework_id)


def test_external_frameworks_never_claim_inferred_crosswalks() -> None:
    snapshot = governance_snapshot()
    for framework_id in ("normenkader-ibp", "mitre-attack"):
        framework = _framework(snapshot, framework_id)
        assert framework["coverage"] == "unmapped"
        assert framework["mapping_ids"] == []
    cvss = _framework(snapshot, "cvss")
    assert cvss["coverage"] == "context_only"
    assert cvss["mapping_ids"] == []


def test_cvss_context_matches_canonical_ingest_contract() -> None:
    schema = Path("backend/dtmo/api/schemas.py").read_text(encoding="utf-8").lower()
    assert "severity:" in schema
    assert "metadata:" in schema
    assert "cvss" not in schema
    cvss = _framework(governance_snapshot(), "cvss")
    assert "geen first-class" in str(cvss["coverage_label"]).lower()


def test_internal_mappings_have_real_repository_provenance() -> None:
    snapshot = governance_snapshot()
    mappings = snapshot["mappings"]
    assert isinstance(mappings, list)
    assert len(mappings) >= 6
    for mapping in mappings:
        source = Path(str(mapping["source"]))
        assert source.is_file(), f"missing governance provenance: {source}"
        contents = source.read_text(encoding="utf-8")
        section = str(mapping["section"])
        if section == "Phase 8/9/10 rows":
            assert "Phase 8" in contents and "Phase 9" in contents and "Phase 10" in contents
        else:
            assert section.lower() in contents.lower()


def test_canonical_governance_surface_preserves_rc13_3_administration() -> None:
    assert 'id="rbac-administration"' in _PAGE
    assert 'id="governance-knowledge"' in _PAGE
    assert 'id="governance-frameworks"' in _PAGE
    assert 'id="governance-mappings"' in _PAGE
    assert 'id="governance-boundaries"' in _PAGE
    assert '/ui/rc13-administration.js' in _PAGE
    assert '/ui/rc13-governance.js' in _PAGE


def test_rc13_4_root_router_precedes_rc13_3_and_unified_console() -> None:
    source = Path("backend/dtmo/main.py").read_text(encoding="utf-8")
    governance = source.index("app.include_router(rc13_governance_router)")
    administration = source.index("app.include_router(rc13_administration_router)")
    unified = source.index("app.include_router(unified_console_router)")
    assert governance < administration < unified
    assert "app.include_router(governance_knowledge_router)" in source
