from dtmo.config import Settings
from dtmo.integration_readiness import integration_readiness
from dtmo.source_catalog import SOURCE_CATALOG


def test_governed_source_catalog_provides_meaningful_bootstrap_content():
    ids = {item.id for item in SOURCE_CATALOG}
    assert len(SOURCE_CATALOG) >= 15
    assert {"cisa-kev", "nvd-cve", "github-global-advisories", "ncsc-nl-advisories", "cert-eu-advisories"} <= ids
    assert all(item.provenance_note.strip() for item in SOURCE_CATALOG)
    assert all(item.endpoint_url.startswith("https://") for item in SOURCE_CATALOG)


def test_default_integrations_explain_disabled_readiness_instead_of_implying_missing_capability():
    rows = {row.id: row for row in integration_readiness(Settings())}
    assert {"misp", "ail", "taranis", "intelowl", "cortex", "opencti", "thehive"} <= rows.keys()
    assert all(row.state == "disabled" for row in rows.values())
    assert all(not row.can_activate for row in rows.values())
    assert all(row.activation_blockers for row in rows.values())
    assert all("Capability exists" in row.detail for row in rows.values())
    assert all(row.action.startswith("Configure") for row in rows.values())


def test_readiness_distinguishes_endpoint_credential_and_enabled_state():
    endpoint_only = Settings(feature_misp_connector=True, misp_api_base="https://misp.example")
    assert {row.id: row for row in integration_readiness(endpoint_only)}["misp"].state == "credential-required"

    enabled_without_endpoint = Settings(feature_opencti_read=True)
    assert {row.id: row for row in integration_readiness(enabled_without_endpoint)}["opencti"].state == "credential-required"

    ready = Settings(feature_misp_connector=True, misp_api_base="https://misp.example", misp_api_key="runtime-secret")
    misp = {row.id: row for row in integration_readiness(ready)}["misp"]
    assert misp.state == "ready"
    assert misp.activation_blockers == ()


def test_configured_disabled_integration_is_server_derived_ready_to_activate():
    configured = Settings(misp_api_base="https://misp.example", misp_api_key="runtime-secret")
    misp = {row.id: row for row in integration_readiness(configured)}["misp"]
    assert misp.state == "disabled"
    assert misp.can_activate is True
    assert misp.activation_blockers == ()
    assert "ready for explicit activation" in misp.detail


def test_component_specific_scope_and_allowlist_requirements_block_activation():
    settings = Settings(
        ail_api_base="https://ail.example",
        ail_api_key="secret",
        intelowl_api_base="https://intelowl.example",
        intelowl_api_token="secret",
        cortex_api_base="https://cortex.example",
        cortex_api_token="secret",
        thehive_api_base="https://thehive.example",
        thehive_api_token="secret",
    )
    rows = {row.id: row for row in integration_readiness(settings)}
    assert "AIL object scope" in rows["ail"].activation_blockers
    assert "IntelOwl analyzer allowlist" in rows["intelowl"].activation_blockers
    assert "Cortex analyzer allowlist" in rows["cortex"].activation_blockers
    assert "TheHive organization scope" in rows["thehive"].activation_blockers
    assert all(not rows[item].can_activate for item in ("ail", "intelowl", "cortex", "thehive"))
