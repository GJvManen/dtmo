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


def test_run_action_is_only_exposed_for_registered_enabled_sources() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    assert "const registered=Boolean(r),enabled=Boolean(r?.enabled)" in text
    assert "run=s?.manual_run_available&&enabled" in text
    assert "Geregistreerd maar uitgeschakeld" in text
    assert "Nog niet geregistreerd" in text


def test_administration_reuses_source_operations_in_same_shell() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    assert 'data-view="administration"' in text
    assert 'data-view="sources">Open bronbeheer</button>' in text
    assert "Operationeel bronbeheer binnen dezelfde applicatieshell" in text
    assert "Administrators kunnen bronnen registreren, valideren, activeren en uitvoeren" in text


def test_source_connection_matrix_has_no_remaining_vendor_adapter_blocker() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    assert "Broadcom/VMware Security Advisories" in text
    assert "| Broadcom/VMware Security Advisories | `broadcom-vmware-vmsa-v1` | CONNECTED |" in text
    assert "ADAPTER_REQUIRED" not in text
    assert "PENDING_CI" not in text
