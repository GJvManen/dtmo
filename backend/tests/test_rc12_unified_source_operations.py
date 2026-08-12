from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSOLE = ROOT / "backend/dtmo/unified_console.py"
MATRIX = ROOT / "docs/qa/SOURCE_CONNECTION_MATRIX.md"


def test_source_operations_are_available_inside_unified_console() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    assert "Registreren, activeren, valideren, interval beheren en feeds laden" in text
    assert "/api/v1/admin/sources/catalog/bootstrap" in text
    assert "/api/v1/admin/sources/${encodeURIComponent(id)}" in text
    assert "/api/v1/admin/sources/${encodeURIComponent(id)}/validate" in text
    assert "/api/v1/admin/sources/${encodeURIComponent(id)}/run" in text
    assert "data-enabled" in text
    assert "data-interval" in text
    assert "data-save" in text
    assert "data-validate" in text
    assert "data-run" in text


def test_run_action_handles_built_in_and_registered_framework_sources() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    assert "const built=c.execution_status==='supported-built-in'" in text
    assert "registered=built||Boolean(s?.registered)||Boolean(r)" in text
    assert "manual=Boolean(s?.manual_run_available)" in text
    assert "run=manual&&(built||enabled)" in text
    assert "Built-in · handmatige run beschikbaar" in text
    assert "Geregistreerd · uitgeschakeld" in text
    assert "Nog niet geregistreerd" in text


def test_administration_links_to_single_source_operations_workspace_without_duplication() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    assert 'data-view="administration"' in text
    assert 'data-view="sources">Open bronbeheer</button>' in text
    assert "Bronbeheer blijft bewust in Bronnen & catalogus" in text
    assert "Bronregistratie en feeduitvoering worden op één plek beheerd" in text
    administration = text.split(
        '<section class="view" data-view-panel="administration">', 1
    )[1].split('<section class="view" data-view-panel="governance">', 1)[0]
    assert 'data-enabled="' not in administration
    assert 'data-run="' not in administration
    assert 'data-save="' not in administration
    assert 'data-validate="' not in administration


def test_source_connection_matrix_has_no_remaining_vendor_adapter_blocker() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    assert "Broadcom/VMware Security Advisories" in text
    assert "| Broadcom/VMware Security Advisories | `broadcom-vmware-vmsa-v1` | CONNECTED |" in text
    assert "ADAPTER_REQUIRED" not in text
    assert "PENDING_CI" not in text
