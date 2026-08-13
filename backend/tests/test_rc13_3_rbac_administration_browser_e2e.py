from __future__ import annotations

import json
import os
from urllib.parse import unquote

import pytest
from playwright.async_api import Route, async_playwright, expect

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC13.3 browser E2E executes only in the dedicated workflow",
)


def _principal(
    subject: str,
    *,
    display_name: str,
    roles: list[str],
    active: bool = True,
    principal_type: str = "human",
) -> dict[str, object]:
    return {
        "subject": subject,
        "display_name": display_name,
        "principal_type": principal_type,
        "active": active,
        "roles": roles,
        "created_by": "admin-tester",
        "updated_by": "admin-tester",
        "created_at": "2026-08-11T16:30:00+00:00",
        "updated_at": "2026-08-11T16:30:00+00:00",
        "requires_token_reissue": True,
        "authorization_note": (
            "Production bearer tokens are externally issued; assignment changes require "
            "identity-provider reconciliation or token reissue and never rewrite active tokens."
        ),
    }


@pytest.mark.asyncio
async def test_canonical_administration_creates_and_updates_role_assignment() -> None:
    roles = [
        {
            "role": "admin",
            "permissions": ["manage:users", "manage:connectors", "approve:share"],
            "eligible_principal_types": ["human"],
            "immutable": True,
        },
        {
            "role": "analyst",
            "permissions": ["read:intelligence", "ingest:intelligence"],
            "eligible_principal_types": ["human"],
            "immutable": True,
        },
        {
            "role": "reviewer",
            "permissions": ["read:intelligence", "review:intelligence"],
            "eligible_principal_types": ["human"],
            "immutable": True,
        },
        {
            "role": "publisher",
            "permissions": ["read:intelligence", "approve:share", "export:reports"],
            "eligible_principal_types": ["human"],
            "immutable": True,
        },
        {
            "role": "service_account",
            "permissions": ["read:intelligence", "ingest:intelligence", "manage:connectors"],
            "eligible_principal_types": ["service_account"],
            "immutable": True,
        },
    ]
    principals = [
        _principal(
            "admin-tester",
            display_name="Current Admin",
            roles=["admin"],
        )
    ]
    mutation_request_ids: list[str] = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "admin-tester",
                "X-DTMO-Roles": "admin",
            }
        )
        page = await context.new_page()

        async def roles_route(route: Route) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(roles),
            )

        async def principals_route(route: Route) -> None:
            if route.request.method == "GET":
                await route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(principals),
                )
                return
            assert route.request.method == "POST"
            mutation_request_ids.append(route.request.headers.get("x-request-id", ""))
            payload = json.loads(route.request.post_data or "{}")
            created = _principal(
                payload["subject"],
                display_name=payload.get("display_name") or payload["subject"],
                roles=payload["roles"],
                active=payload["active"],
                principal_type=payload["principal_type"],
            )
            principals.append(created)
            await route.fulfill(
                status=201,
                content_type="application/json",
                body=json.dumps(created),
            )

        async def principal_update_route(route: Route) -> None:
            mutation_request_ids.append(route.request.headers.get("x-request-id", ""))
            payload = json.loads(route.request.post_data or "{}")
            if route.request.url.endswith("/governed-assignment"):
                assert route.request.method == "POST"
                subject = unquote(route.request.url.rsplit("/", 2)[-2])
                assert len(payload["reason"].strip()) >= 3
            else:
                assert route.request.method == "PATCH"
                subject = unquote(route.request.url.rsplit("/", 1)[-1])
            current = next(item for item in principals if item["subject"] == subject)
            current["display_name"] = payload.get("display_name") or current["display_name"]
            current["active"] = payload["active"]
            current["roles"] = payload["roles"]
            current["updated_at"] = "2026-08-11T16:40:00+00:00"
            if route.request.url.endswith("/governed-assignment"):
                request_id = route.request.headers.get("x-request-id", "")
                await route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(
                        {
                            "principal": current,
                            "reason": payload["reason"],
                            "request_id": request_id,
                            "before": "fixture-before",
                            "after": "fixture-after",
                            "authorization_note": "Governed fixture response",
                        }
                    ),
                )
                return
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(current),
            )

        async def empty_list_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body="[]")

        async def dashboard_route(route: Route) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(
                    {
                        "total_intelligence": 0,
                        "new_last_24h": 0,
                        "average_confidence": 0,
                        "severity": {},
                        "sources": {},
                        "connector_health": {},
                        "review_status": {},
                        "intelligence_trend_7d": {},
                    }
                ),
            )

        await page.route("**/api/v1/admin/rbac/roles", roles_route)
        await page.route("**/api/v1/admin/rbac/principals", principals_route)
        await page.route("**/api/v1/admin/rbac/principals/*", principal_update_route)
        await page.route("**/api/v1/admin/sources/catalog", empty_list_route)
        await page.route("**/api/v1/source-center/status", empty_list_route)
        await page.route("**/api/v1/admin/sources", empty_list_route)
        await page.route("**/api/v1/console/recent-intelligence?*", empty_list_route)
        await page.route("**/api/v1/dashboards/summary", dashboard_route)

        await page.goto(f"{BASE_URL}/")
        await page.get_by_role("button", name="Administration").click()

        panel = page.locator("#rbac-administration")
        await expect(panel).to_be_visible()
        await expect(panel).to_contain_text("Gebruikers & rollen")
        await expect(page.locator("#rbac-role-catalog")).to_contain_text("manage:users")
        await expect(page.locator('[data-rbac-principal="admin-tester"]')).to_contain_text(
            "Zelfbeheer is server-side geblokkeerd"
        )
        await expect(
            page.locator('[data-rbac-principal="admin-tester"] [data-rbac-save]')
        ).to_be_disabled()

        await page.locator("#rbac-subject").fill("reviewer@example.test")
        await page.locator("#rbac-display-name").fill("Education Reviewer")
        await page.locator('#rbac-create-roles [data-rbac-role="reviewer"]').check()
        await page.get_by_role("button", name="Principal aanmaken").click()

        created = page.locator('[data-rbac-principal="reviewer@example.test"]')
        await expect(created).to_be_visible()
        await expect(created).to_contain_text("Education Reviewer")
        await expect(created).to_contain_text("token reissue: vereist")
        await expect(page.locator("#rbac-status")).to_contain_text(
            "Identity-provider/tokenreconciliatie is vereist"
        )

        await created.locator('[data-rbac-role="reviewer"]').uncheck()
        await created.locator('[data-rbac-role="publisher"]').check()
        await created.locator("[data-rbac-active]").uncheck()
        await expect(created.locator("[data-e6-rbac-save]")).to_have_text("Governed opslaan")
        await created.locator("[data-e6-reason]").fill(
            "Reviewer assignment moved to inactive publisher for RC13 acceptance."
        )
        await created.locator("[data-e6-rbac-save]").click()

        updated = page.locator('[data-rbac-principal="reviewer@example.test"]')
        await expect(updated).to_contain_text("Inactief")
        await expect(updated.locator('[data-rbac-role="publisher"]')).to_be_checked()
        await expect(updated.locator('[data-rbac-role="reviewer"]')).not_to_be_checked()
        await expect(updated.locator("[data-rbac-result]")).to_contain_text(
            "Opgeslagen en geaudit"
        )

        assert len(mutation_request_ids) == 2
        assert all(mutation_request_ids)
        assert len(set(mutation_request_ids)) == 2

        await context.close()
        await browser.close()
