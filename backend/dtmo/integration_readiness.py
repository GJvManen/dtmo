from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from dtmo.config import Settings

ReadinessState = Literal["ready", "credential-required", "configuration-required", "disabled", "reference-only"]


@dataclass(frozen=True, slots=True)
class IntegrationReadiness:
    id: str
    name: str
    state: ReadinessState
    enabled: bool
    configured: bool
    credential_configured: bool
    can_activate: bool
    activation_blockers: tuple[str, ...]
    action: str
    detail: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _secret_present(value: object) -> bool:
    getter = getattr(value, "get_secret_value", None)
    raw = getter() if callable(getter) else value
    return bool(str(raw or "").strip())


def _component_blockers(settings: Settings, integration_id: str) -> list[str]:
    blockers: list[str] = []
    if integration_id == "ail" and not settings.ail_object_global_ids.strip():
        blockers.append("AIL object scope")
    elif integration_id == "intelowl" and not settings.intelowl_allowed_analyzers.strip():
        blockers.append("IntelOwl analyzer allowlist")
    elif integration_id == "cortex" and not settings.cortex_allowed_analyzers.strip():
        blockers.append("Cortex analyzer allowlist")
    elif integration_id == "opencti":
        if not settings.opencti_allowed_entity_types.strip():
            blockers.append("OpenCTI entity-type allowlist")
        if not settings.opencti_checkpoint_path.strip():
            blockers.append("OpenCTI checkpoint path")
    elif integration_id == "thehive" and not settings.thehive_organization.strip():
        blockers.append("TheHive organization scope")
    return blockers


def integration_readiness(settings: Settings) -> tuple[IntegrationReadiness, ...]:
    specs = (
        ("misp", "MISP", settings.feature_misp_connector, settings.misp_api_base, settings.misp_api_key, "Configure MISP API base/key and enable the connector."),
        ("ail", "AIL", settings.feature_ail_connector, settings.ail_api_base, settings.ail_api_key, "Configure AIL API base/key, object scope and enable the connector."),
        ("taranis", "Taranis AI", settings.feature_taranis_connector, settings.taranis_api_base, settings.taranis_api_token, "Configure Taranis API base/token and enable the connector."),
        ("intelowl", "IntelOwl", settings.feature_intelowl_enrichment, settings.intelowl_api_base, settings.intelowl_api_token, "Configure IntelOwl API base/token and analyzer allowlist."),
        ("cortex", "Cortex", settings.feature_cortex_analysis, settings.cortex_api_base, settings.cortex_api_token, "Configure Cortex API base/token and analyzer allowlist."),
        ("opencti", "OpenCTI", settings.feature_opencti_read, settings.opencti_api_base, settings.opencti_api_token, "Configure OpenCTI API base/token and enable governed read access."),
        ("thehive", "TheHive", settings.feature_thehive_handoff, settings.thehive_api_base, settings.thehive_api_token, "Configure TheHive API base/token, organization and enable handoff."),
    )
    rows: list[IntegrationReadiness] = []
    for integration_id, name, enabled, api_base, credential, action in specs:
        configured = bool(api_base.strip())
        credential_configured = _secret_present(credential)
        blockers: list[str] = []
        if not configured:
            blockers.append("API endpoint")
        if not credential_configured:
            blockers.append("server-side credential")
        blockers.extend(_component_blockers(settings, integration_id))
        can_activate = not blockers

        if enabled and can_activate:
            state: ReadinessState = "ready"
            detail = "Enabled and required runtime configuration is present. Runtime health remains a separate signal."
        elif enabled and configured and not credential_configured and len(blockers) == 1:
            state = "credential-required"
            detail = "Enabled and endpoint configured, but runtime credential is missing."
        elif enabled:
            state = "configuration-required"
            detail = "Enabled, but required runtime configuration is incomplete: " + ", ".join(blockers) + "."
        else:
            state = "disabled"
            if can_activate:
                detail = "Required runtime configuration is present; explicit governed activation is still required."
            else:
                detail = "Capability exists but remains disabled until governed runtime configuration is complete: " + ", ".join(blockers) + "."

        rows.append(
            IntegrationReadiness(
                integration_id,
                name,
                state,
                bool(enabled),
                configured,
                credential_configured,
                can_activate,
                tuple(blockers),
                action,
                detail,
            )
        )
    return tuple(rows)
