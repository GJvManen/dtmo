from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Route, async_playwright

ADMIN_ROUTE = "/workbench/administration"
VIEWPORT = {"width": 1440, "height": 1000}


def _json(route: Route, payload: object) -> None:
    asyncio.create_task(route.fulfill(status=200, content_type="application/json", body=json.dumps(payload)))


def session_fixture() -> dict[str, object]:
    return {
        "subject": "documentation-admin@example.invalid",
        "roles": ["administrator"],
        "permissions": ["manage:connectors", "manage:users", "read:intelligence"],
    }


def integrations_fixture() -> list[dict[str, object]]:
    return [
        {
            "id": "misp",
            "name": "MISP",
            "enabled": True,
            "api_base": "https://misp.example.invalid",
            "credential_configured": True,
            "state": "ready",
            "can_activate": True,
            "activation_blockers": [],
            "ail_object_global_ids": "",
            "intelowl_allowed_analyzers": "",
            "cortex_allowed_analyzers": "",
            "opencti_allowed_entity_types": "",
            "opencti_checkpoint_path": "",
            "thehive_organization": "",
            "credential_boundary": "Credential values remain server-side and are never returned to the browser.",
        },
        {
            "id": "opencti",
            "name": "OpenCTI",
            "enabled": False,
            "api_base": "https://opencti.example.invalid",
            "credential_configured": False,
            "state": "configuration-required",
            "can_activate": False,
            "activation_blockers": ["entity type allowlist required"],
            "ail_object_global_ids": "",
            "intelowl_allowed_analyzers": "",
            "cortex_allowed_analyzers": "",
            "opencti_allowed_entity_types": "Indicator,Malware",
            "opencti_checkpoint_path": "/var/lib/dtmo/opencti.checkpoint",
            "thehive_organization": "",
            "credential_boundary": "Credential values remain server-side and are never returned to the browser.",
        },
    ]


def roles_fixture() -> list[dict[str, object]]:
    return [
        {"role": "analyst", "permissions": ["read:intelligence", "review:intelligence"], "eligible_principal_types": ["human"], "immutable": True},
        {"role": "administrator", "permissions": ["manage:users", "manage:connectors"], "eligible_principal_types": ["human"], "immutable": True},
        {"role": "connector-service", "permissions": ["manage:connectors"], "eligible_principal_types": ["service_account"], "immutable": True},
    ]


def principals_fixture() -> list[dict[str, object]]:
    return [
        {
            "subject": "alice@example.invalid",
            "display_name": "Alice Analyst",
            "principal_type": "human",
            "active": True,
            "roles": ["analyst"],
            "requires_token_reissue": False,
            "authorization_note": "Existing bearer tokens retain their original claims until reissued.",
        },
        {
            "subject": "svc-collector@example.invalid",
            "display_name": "Collection Service",
            "principal_type": "service_account",
            "active": True,
            "roles": ["connector-service"],
            "requires_token_reissue": False,
            "authorization_note": "Service accounts are excluded from human review/share authority.",
        },
    ]


def matrix_fixture() -> dict[str, object]:
    return {
        "separation_of_duties": [
            "Review and external-share approval remain separate human authorities.",
            "Service accounts cannot exercise human review or share approval authority.",
            "UI visibility never grants server-side permissions.",
        ],
        "immutable_policy": True,
    }


async def install_routes(page) -> None:
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/admin/integrations", lambda route: _json(route, integrations_fixture()))
    await page.route("**/api/v1/admin/rbac/roles", lambda route: _json(route, roles_fixture()))
    await page.route("**/api/v1/admin/rbac/principals", lambda route: _json(route, principals_fixture()))
    await page.route("**/api/v1/admin/rbac/matrix", lambda route: _json(route, matrix_fixture()))


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        await page.goto(base_url.rstrip("/") + ADMIN_ROUTE, wait_until="networkidle")

        await page.get_by_role("heading", name="Administration", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Governed configuration and identity", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Runtime configuration", exact=True).wait_for(state="visible")
        await page.get_by_text("Credentials and authorization policy remain server-side", exact=False).wait_for(state="visible")

        candidate_filename = "administration-rbac-workbench.png"
        await page.screenshot(path=str(output / candidate_filename), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": ADMIN_ROUTE,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "canonical administration -> integration configuration -> identity/RBAC -> separation-of-duties boundary",
            "fixture_backed": True,
            "credential_value_exposed": False,
            "mutation_executed": False,
            "rbac_enforcement_proven": False,
            "token_reissue_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "independent_assurance_proven": False,
            "review_authority_proven": False,
            "share_authority_proven": False,
            "production_authority_proven": False,
            "files": [candidate_filename],
        }
        (output / "canonical-administration-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture canonical DTMO UI-09 Administration/RBAC documentation screenshot.")
    parser.add_argument("--base-url", required=True, help="Running DTMO canonical base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
