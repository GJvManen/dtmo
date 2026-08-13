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
    reason="RC13.5 browser E2E executes only in the dedicated workflow",
)


def _principal(
    subject: str,
    *,
    display_name: str,
    roles: list[str],
    active: bool = True,
) -> dict[str, object]:
    return {
        "subject": subject,
        "display_name": display_name,
        "principal_type": "human",
        "active": active,
        "roles": roles,
        "created_by": "admin-tester",
        "updated_by": "admin-tester",
        "created_at": "2026-08-11T18:00:00+00:00",
        "updated_at": "2026-08-11T18:00:00+00:00",
        "requires_token_reissue": True,
        "authorization_note": (
            "Production bearer tokens are externally issued; assignment changes require "
            "identity-provider reconciliation or token reissue and never rewrite active tokens."
        ),
    }


@pytest.mark.asyncio
async def test_complete_canonical_console_journey_in_one_browser_session() -> None:
    source_state = {"registered": False, "enabled": False, "ingested": False}
    principals = [_principal("admin-tester", display_name="Current Admin", roles=["admin"])]
    mutation_request_ids: list[str] = []
    grafana_requests: list[str] = []
    external_requests: list[str] = []

    catalog = [
        {
            "id": "cisa-kev",
            "name": "CISA Known Exploited Vulnerabilities",
            "endpoint_url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
            "reliability": "authoritative",
            "category": "exploited-vulnerabilities",
            "execution_profile": "built-in-cisa-kev",
            "execution_status": "supported-built-in",
            "provenance_note": "RC13.5 synthetic fixture",
            "recommended_interval_seconds": 3600,
            "secret_ref": None,
        },
        {
            "id": "nvd-cve",
            "name": "NIST NVD CVE API 2.0",
            "endpoint_url": "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=100",
            "reliability": "authoritative",
            "category": "vulnerabilities",
            "execution_profile": "nvd-cve-v2",
            "execution_status": "supported",
            "provenance_note": "RC13.5 synthetic fixture",
            "recommended_interval_seconds": 7200,
            "secret_ref": None,
        },
    ]

    roles = [
        {
            "role": "admin",
            "permissions": ["manage:users", "manage:connectors", "approve:share"],
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
    ]

    def registered_sources() -> list[dict[str, object]]:
        if not source_state["registered"]:
            return []
        return [
            {
                "id": "nvd-cve",
                "name": "NIST NVD CVE API 2.0",
                "source_type": "json-feed",
                "endpoint_url": catalog[1]["endpoint_url"],
                "enabled": source_state["enabled"],
                "interval_seconds": 7200,
                "reliability": "authoritative",
                "secret_ref": None,
                "created_by": "admin-tester",
                "updated_by": "admin-tester",
            }
        ]

    def source_status() -> list[dict[str, object]]:
        return [
            {
                "id": "cisa-kev",
                "name": "CISA Known Exploited Vulnerabilities",
                "category": "exploited-vulnerabilities",
                "source_type": "cisa-kev",
                "execution_profile": "built-in-cisa-kev",
                "execution_status": "supported-built-in",
                "registered": True,
                "enabled": False,
                "interval_seconds": 3600,
                "reliability": "authoritative",
                "health_status": "healthy" if source_state["ingested"] else "unknown",
                "last_success_at": "2026-08-11T18:01:00+00:00" if source_state["ingested"] else None,
                "last_failure_at": None,
                "consecutive_failures": 0,
                "isolated_until": None,
                "manual_run_available": True,
                "provenance": {"endpoint": catalog[0]["endpoint_url"]},
            },
            {
                "id": "nvd-cve",
                "name": "NIST NVD CVE API 2.0",
                "category": "vulnerabilities",
                "source_type": "json-feed",
                "execution_profile": "nvd-cve-v2",
                "execution_status": "supported",
                "registered": source_state["registered"],
                "enabled": source_state["enabled"],
                "interval_seconds": 7200,
                "reliability": "authoritative",
                "health_status": "healthy" if source_state["ingested"] else "unknown",
                "last_success_at": "2026-08-11T18:01:00+00:00" if source_state["ingested"] else None,
                "last_failure_at": None,
                "consecutive_failures": 0,
                "isolated_until": None,
                "manual_run_available": source_state["registered"] and source_state["enabled"],
                "provenance": {"endpoint": catalog[1]["endpoint_url"]},
            },
        ]

    def recent_items() -> list[dict[str, object]]:
        if not source_state["ingested"]:
            return []
        return [
            {
                "id": "55555555-5555-5555-5555-555555555555",
                "source_id": "nvd-cve",
                "title": "RC13.5 synthetic NVD advisory",
                "summary": "One-session canonical-console acceptance fixture",
                "severity": "high",
                "confidence_score": 92,
                "education_relevance": 88,
                "review_status": "candidate",
                "share_approved": False,
                "canonical_url": "https://example.invalid/RC13-5",
                "published_at": None,
                "discovered_at": "2026-08-11T18:01:00+00:00",
            }
        ]

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "admin-tester",
                "X-DTMO-Roles": "admin",
            }
        )
        page = await context.new_page()

        async def catalog_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body=json.dumps(catalog))

        async def status_route(route: Route) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(source_status()),
            )

        async def registered_route(route: Route) -> None:
            if route.request.method == "GET":
                await route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(registered_sources()),
                )
                return
            await route.fallback()

        async def bootstrap_route(route: Route) -> None:
            source_state["registered"] = True
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(registered_sources()),
            )

        async def nvd_route(route: Route) -> None:
            assert route.request.method == "PATCH"
            payload = json.loads(route.request.post_data or "{}")
            source_state["enabled"] = bool(payload.get("enabled"))
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(registered_sources()[0]),
            )

        async def nvd_run_route(route: Route) -> None:
            source_state["ingested"] = True
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(
                    {
                        "id": "nvd-cve",
                        "status": "completed",
                        "records": 1,
                        "inserted": 1,
                        "indexed": 1,
                        "error": None,
                        "publication_gate": "human-review-and-separate-share-approval-required",
                    }
                ),
            )

        async def recent_route(route: Route) -> None:
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(recent_items()),
            )

        async def dashboard_route(route: Route) -> None:
            total = 1 if source_state["ingested"] else 0
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(
                    {
                        "generated_at": "2026-08-11T18:01:00+00:00",
                        "total_intelligence": total,
                        "new_last_24h": total,
                        "average_confidence": 92.0 if total else 0.0,
                        "severity": {"high": total} if total else {},
                        "review_status": {"candidate": total} if total else {},
                        "sources": {"nvd-cve": total} if total else {},
                        "connector_health": {"healthy": 2} if total else {"unknown": 2},
                        "intelligence_trend_7d": {
                            "2026-08-05": 0,
                            "2026-08-06": 0,
                            "2026-08-07": 0,
                            "2026-08-08": 0,
                            "2026-08-09": 0,
                            "2026-08-10": 0,
                            "2026-08-11": total,
                        },
                    }
                ),
            )

        async def roles_route(route: Route) -> None:
            await route.fulfill(status=200, content_type="application/json", body=json.dumps(roles))

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
            )
            principals.append(created)
            await route.fulfill(status=201, content_type="application/json", body=json.dumps(created))

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
            current["updated_at"] = "2026-08-11T18:02:00+00:00"
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
            await route.fulfill(status=200, content_type="application/json", body=json.dumps(current))

        await page.route("**/api/v1/admin/sources/catalog", catalog_route)
        await page.route("**/api/v1/source-center/status", status_route)
        await page.route("**/api/v1/admin/sources", registered_route)
        await page.route("**/api/v1/admin/sources/catalog/bootstrap", bootstrap_route)
        await page.route("**/api/v1/admin/sources/nvd-cve", nvd_route)
        await page.route("**/api/v1/admin/sources/nvd-cve/run", nvd_run_route)
        await page.route("**/api/v1/console/recent-intelligence?*", recent_route)
        await page.route("**/api/v1/dashboards/summary", dashboard_route)
        await page.route("**/api/v1/admin/rbac/roles", roles_route)
        await page.route("**/api/v1/admin/rbac/principals", principals_route)
        await page.route(
            "**/api/v1/admin/rbac/principals/*/governed-assignment",
            principal_update_route,
        )
        await page.route("**/api/v1/admin/rbac/principals/*", principal_update_route)

        def observe_request(request: object) -> None:
            url = str(getattr(request, "url", ""))
            if "/grafana/" in url:
                grafana_requests.append(url)
            if url and not url.startswith(BASE_URL):
                external_requests.append(url)

        page.on("request", observe_request)

        await page.goto(f"{BASE_URL}/")

        # 1. Overview: native product state and charts exist before any source run.
        await expect(page.locator('[data-view-panel="overview"]')).to_be_visible()
        await expect(page.locator("#overview-trend-chart")).to_be_visible()
        await expect(page.locator("#overview-severity-chart")).to_be_visible()
        await expect(page.locator("#overview-connector-chart")).to_be_visible()
        await expect(page.get_by_test_id("overview-recent")).to_contain_text(
            "Nog geen intelligence ingested"
        )

        # 2. Intelligence: canonical recent-intelligence view is usable without a search first.
        await page.get_by_role("button", name="Intelligence", exact=True).click()
        await expect(page.locator('[data-view-panel="intelligence"]')).to_be_visible()
        await expect(page.get_by_test_id("intel-recent")).to_contain_text(
            "Nog geen intelligence ingested"
        )

        # 3. Sources & Catalog: register, enable and execute a connected framework source.
        await page.get_by_role("button", name="Bronnen & catalogus").click()
        nvd = page.locator('[data-source-card="nvd-cve"]')
        await expect(nvd).to_contain_text("Nog niet geregistreerd")
        await page.get_by_role("button", name="Frameworkbronnen registreren").click()
        await expect(nvd.get_by_text("Geregistreerd · uitgeschakeld")).to_be_visible()
        await nvd.locator('input[data-enabled="nvd-cve"]').check()
        await nvd.get_by_role("button", name="Opslaan").click()
        await expect(nvd.get_by_text("Operationeel")).to_be_visible()
        await nvd.get_by_role("button", name="Feed nu laden").click()
        await expect(nvd.locator('[data-result="nvd-cve"]')).to_contain_text(
            "completed: 1 records, 1 inserted, 1 indexed"
        )

        # The source result must flow back into canonical Intelligence in the same browser session.
        await page.get_by_role("button", name="Intelligence", exact=True).click()
        await expect(page.get_by_test_id("intel-recent")).to_contain_text(
            "RC13.5 synthetic NVD advisory"
        )

        # 4. Visual analytics: native severity/source/connector/review views use the same session.
        await page.get_by_role("button", name="Visual analytics").click()
        await expect(page.locator('[data-view-panel="analytics"]')).to_be_visible()
        for selector in ("#severity-chart", "#source-chart", "#connector-chart", "#review-chart"):
            await expect(page.locator(selector)).to_be_visible()
        await expect(page.locator("#severity-table")).to_contain_text("high")
        await expect(page.locator("#source-table")).to_contain_text("nvd-cve")
        await expect(page.locator("#connector-table")).to_contain_text("healthy")
        await expect(page.locator("#review-table")).to_contain_text("candidate")
        assert grafana_requests == []

        # 5. Administration: governed RBAC remains functional in the same canonical shell.
        await page.get_by_role("button", name="Administration").click()
        panel = page.locator("#rbac-administration")
        await expect(panel).to_be_visible()
        await expect(page.locator("#rbac-role-catalog")).to_contain_text("manage:users")
        await expect(page.locator('[data-rbac-principal="admin-tester"] [data-rbac-save]')).to_be_disabled()

        await page.locator("#rbac-subject").fill("rc13-reviewer@example.test")
        await page.locator("#rbac-display-name").fill("RC13 Reviewer")
        await page.locator('#rbac-create-roles [data-rbac-role="reviewer"]').check()
        await page.get_by_role("button", name="Principal aanmaken").click()
        managed = page.locator('[data-rbac-principal="rc13-reviewer@example.test"]')
        await expect(managed).to_contain_text("token reissue: vereist")
        await managed.locator('[data-rbac-role="reviewer"]').uncheck()
        await managed.locator('[data-rbac-role="publisher"]').check()
        await managed.locator("[data-rbac-active]").uncheck()
        await expect(managed.locator("[data-e6-rbac-save]")).to_have_text("Governed opslaan")
        await managed.locator("[data-e6-reason]").fill(
            "Reviewer assignment moved to inactive publisher in full-console acceptance."
        )
        await managed.locator("[data-e6-rbac-save]").click()
        await expect(managed).to_contain_text("Inactief")
        await expect(managed.locator('[data-rbac-role="publisher"]')).to_be_checked()
        await expect(managed.locator("[data-rbac-result]")).to_contain_text("Opgeslagen en geaudit")
        assert len(mutation_request_ids) == 2
        assert all(mutation_request_ids)
        assert len(set(mutation_request_ids)) == 2

        # 6. Governance: framework coverage, provenance and authority boundaries are visible.
        await page.get_by_role("button", name="Governance").click()
        governance = page.locator("#governance-knowledge")
        await expect(governance).to_be_visible()
        await expect(page.locator('[data-governance-framework="normenkader-ibp"]')).to_contain_text(
            "Nog niet gemapt"
        )
        await expect(page.locator('[data-governance-framework="mitre-attack"]')).to_contain_text(
            "Nog niet gemapt"
        )
        await expect(page.locator('[data-governance-framework="cvss"]')).to_contain_text(
            "Context, geen first-class score"
        )
        await expect(page.locator('[data-governance-mapping="exact-head-evidence"]')).to_contain_text(
            "Exact-head release evidence"
        )
        await expect(page.locator("#governance-boundaries")).to_contain_text(
            "publication/share authority"
        )

        # Close the loop: Overview reflects the source operation performed earlier in this same session.
        await page.get_by_role("button", name="Overzicht").click()
        await expect(page.locator("#kpi-intel")).to_have_text("1")
        await expect(page.get_by_test_id("overview-recent")).to_contain_text(
            "RC13.5 synthetic NVD advisory"
        )

        assert grafana_requests == []
        assert external_requests == []

        await context.close()
        await browser.close()
