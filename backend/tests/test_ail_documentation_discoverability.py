from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCH = ROOT / "docs/architecture/SYSTEM_ARCHITECTURE.md"
READ = ROOT / "docs/integrations/AIL_READ_ENRICHMENT.md"
CORRELATION = ROOT / "docs/integrations/AIL_CORRELATION_EXPERIENCE.md"
OPERATOR = ROOT / "docs/user/AIL_CORRELATION_WORKSPACE.md"


def test_ail_is_documented_across_architecture_integration_and_operator_domains():
    assert "AIL" in ARCH.read_text(encoding="utf-8")
    assert READ.exists()
    assert CORRELATION.exists()
    operator = OPERATOR.read_text(encoding="utf-8")
    for marker in (
        "first-class governed framework building block",
        "browser → same-origin DTMO API → governed AIL adapter → AIL",
        "Credentials remain server-side",
        "fail-closed",
        "does not prove live AIL connectivity",
        "does not establish owner acceptance",
    ):
        assert marker.lower() in operator.lower(), marker


def test_ail_operator_guide_links_stable_contracts_without_granting_authority():
    operator = OPERATOR.read_text(encoding="utf-8")
    for path in (
        "docs/architecture/SYSTEM_ARCHITECTURE.md",
        "docs/integrations/AIL_READ_ENRICHMENT.md",
        "docs/integrations/AIL_CORRELATION_EXPERIENCE.md",
    ):
        assert path in operator, path
    assert "grant review, case, sharing or publication authority" in operator
