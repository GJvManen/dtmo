from pathlib import Path

import dtmo.admin_center as admin
from dtmo.config import Settings


def test_integration_settings_are_actionable_and_never_return_secret_values(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(admin, "settings", Settings())
    monkeypatch.setattr(admin, "_RUNTIME_CONFIG_PATH", tmp_path / "runtime-integration-settings.json")
    monkeypatch.setattr(admin, "_RUNTIME_SECRET_PATH", tmp_path / "runtime-integration-secrets.json")

    before = {row["id"]: row for row in admin.list_integrations(None)}
    assert before["misp"]["state"] == "disabled"
    assert "credential_boundary" in before["misp"]
    assert "credential" not in before["misp"]
    assert "api_key" not in before["misp"]
    assert "token" not in before["misp"]

    updated = admin.update_integration(
        "misp",
        admin.IntegrationPatch(enabled=True, api_base="https://misp.example/api/", credential="runtime-secret"),
        None,
    )
    assert updated["enabled"] is True
    assert updated["api_base"] == "https://misp.example/api"
    assert updated["credential_configured"] is True
    assert updated["state"] == "ready"
    assert "credential" not in updated

    assert admin._RUNTIME_CONFIG_PATH.exists()
    nonsecret_document = admin._RUNTIME_CONFIG_PATH.read_text(encoding="utf-8")
    assert "misp.example/api" in nonsecret_document
    assert "runtime-secret" not in nonsecret_document

    assert admin._RUNTIME_SECRET_PATH.exists()
    secret_document = admin._RUNTIME_SECRET_PATH.read_text(encoding="utf-8")
    assert "runtime-secret" in secret_document
    assert admin._RUNTIME_SECRET_PATH.stat().st_mode & 0o777 == 0o600


def test_persisted_configuration_and_write_only_credential_are_reapplied(tmp_path: Path, monkeypatch):
    config_path = tmp_path / "runtime-integration-settings.json"
    secret_path = tmp_path / "runtime-integration-secrets.json"
    config_path.write_text('{"opencti":{"enabled":true,"api_base":"https://opencti.example"}}', encoding="utf-8")
    secret_path.write_text('{"opencti":"server-secret"}', encoding="utf-8")
    settings = Settings()
    monkeypatch.setattr(admin, "settings", settings)
    monkeypatch.setattr(admin, "_RUNTIME_CONFIG_PATH", config_path)
    monkeypatch.setattr(admin, "_RUNTIME_SECRET_PATH", secret_path)

    admin._apply_persisted_runtime_configuration()
    assert settings.feature_opencti_read is True
    assert settings.opencti_api_base == "https://opencti.example"
    row = admin._integration_row("opencti")
    assert row["credential_configured"] is True
    assert row["state"] == "ready"
    assert "server-secret" not in str(row)


def test_ail_scope_is_nonsecret_persisted_configuration_and_required_for_ready_state(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(admin, "settings", Settings())
    monkeypatch.setattr(admin, "_RUNTIME_CONFIG_PATH", tmp_path / "runtime-integration-settings.json")
    monkeypatch.setattr(admin, "_RUNTIME_SECRET_PATH", tmp_path / "runtime-integration-secrets.json")

    incomplete = admin.update_integration(
        "ail",
        admin.IntegrationPatch(enabled=True, api_base="https://ail.example", credential="ail-secret"),
        None,
    )
    assert incomplete["state"] == "configuration-required"
    assert "AIL object scope" in incomplete["activation_blockers"]
    assert incomplete["can_activate"] is False

    ready = admin.update_integration(
        "ail",
        admin.IntegrationPatch(ail_object_global_ids=" domain:None:example.org , ip:None:203.0.113.10 "),
        None,
    )
    assert ready["state"] == "ready"
    assert ready["activation_blockers"] == []
    assert ready["ail_object_global_ids"] == "domain:None:example.org,ip:None:203.0.113.10"

    nonsecret_document = admin._RUNTIME_CONFIG_PATH.read_text(encoding="utf-8")
    assert "domain:None:example.org" in nonsecret_document
    assert "ail-secret" not in nonsecret_document
    assert "ail-secret" in admin._RUNTIME_SECRET_PATH.read_text(encoding="utf-8")


def test_empty_credential_and_unknown_integration_fail_closed(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(admin, "settings", Settings())
    monkeypatch.setattr(admin, "_RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setattr(admin, "_RUNTIME_SECRET_PATH", tmp_path / "secrets.json")
    try:
        admin.update_integration("misp", admin.IntegrationPatch(credential="   "), None)
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 422
    else:
        raise AssertionError("empty credential must fail closed")

    try:
        admin.update_integration("unknown", admin.IntegrationPatch(enabled=True), None)
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 404
    else:
        raise AssertionError("unknown integration must fail closed")


def test_ail_scope_is_rejected_for_other_integrations(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(admin, "settings", Settings())
    monkeypatch.setattr(admin, "_RUNTIME_CONFIG_PATH", tmp_path / "runtime.json")
    monkeypatch.setattr(admin, "_RUNTIME_SECRET_PATH", tmp_path / "secrets.json")
    try:
        admin.update_integration("misp", admin.IntegrationPatch(ail_object_global_ids="domain:None:example.org"), None)
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 422
    else:
        raise AssertionError("AIL object scope must fail closed for non-AIL integrations")
