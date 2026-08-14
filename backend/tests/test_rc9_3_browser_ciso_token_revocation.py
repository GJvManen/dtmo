from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import select

from dtmo.audit.store import verify_persistent_audit_chain
from dtmo.auth.token_state import TokenStateStore
from dtmo.config import get_settings
from dtmo.persistence.audit_models import AuditEventRecord
from dtmo.persistence.session import Database

BASE_URL = os.environ.get("DTMO_CISO_E2E_BASE_URL", "http://127.0.0.1:8765")
E2E_ENABLED = bool(os.environ.get("DTMO_CISO_E2E_BASE_URL"))

pytestmark = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="RC9.3 browser E2E executes only in the dedicated CISO browser workflow",
)


async def _assert_revocation_persisted(jti: str) -> None:
    settings = get_settings()
    store = TokenStateStore.from_url(settings.redis_url)
    assert store.is_revoked(jti) is True

    database = Database(settings)
    try:
        async for session in database.session():
            event: AuditEventRecord | None = None
            # The HTTP response can reach Chromium just before FastAPI finishes
            # the request-scoped database dependency and commits the audit row.
            # Keep the evidence requirement strict, but allow that bounded commit
            # hand-off to become visible instead of racing it with a one-shot read.
            for _ in range(40):
                event = await session.scalar(
                    select(AuditEventRecord).where(
                        AuditEventRecord.principal == "carol-ciso",
                        AuditEventRecord.action == "token.revoke",
                        AuditEventRecord.resource == f"token:jti:{jti}",
                    )
                )
                if event is not None:
                    break
                await asyncio.sleep(0.05)

            assert event is not None, "token revocation audit event was not durably persisted"
            assert event.decision == "allow"
            assert event.principal_type == "human"
            assert event.provenance_reference is not None
            assert "RC9.3 synthetic compromised token" in event.provenance_reference
            valid, error = await session.run_sync(verify_persistent_audit_chain)
            assert valid is True, error
            break
    finally:
        await database.close()


@pytest.mark.asyncio
async def test_ciso_browser_revokes_token_while_analyst_is_denied() -> None:
    jti = f"rc9-3-{uuid4()}"
    expires_at = (datetime.now(UTC) + timedelta(hours=2)).isoformat()
    reason = "RC9.3 synthetic compromised token"

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        analyst_context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "alice-analyst",
                "X-DTMO-Roles": "analyst",
            }
        )
        analyst_page = await analyst_context.new_page()
        await analyst_page.goto(f"{BASE_URL}/ui/ciso-security")
        await expect(analyst_page.get_by_test_id("ciso-principal")).to_contain_text("alice-analyst")
        await expect(analyst_page.get_by_test_id("revocation-panel")).to_be_hidden()
        await expect(analyst_page.get_by_test_id("revocation-status")).to_have_attribute(
            "data-state", "forbidden"
        )
        denied_status = await analyst_page.evaluate(
            """async ({jti, expiresAt, reason}) => {
              const response = await fetch('/api/v1/security/tokens/revoke', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {'Content-Type': 'application/json', 'X-Request-ID': crypto.randomUUID()},
                body: JSON.stringify({jti, expires_at: expiresAt, reason}),
              });
              return response.status;
            }""",
            {"jti": jti, "expiresAt": expires_at, "reason": reason},
        )
        assert denied_status == 403
        await analyst_context.close()

        ciso_context = await browser.new_context(
            extra_http_headers={
                "X-DTMO-Subject": "carol-ciso",
                "X-DTMO-Roles": "ciso",
            }
        )
        ciso_page = await ciso_context.new_page()
        await ciso_page.goto(f"{BASE_URL}/ui/ciso-security")
        await expect(ciso_page.get_by_test_id("ciso-principal")).to_contain_text("carol-ciso")
        await expect(ciso_page.get_by_test_id("revocation-panel")).to_be_visible()
        await expect(ciso_page.get_by_test_id("revocation-status")).to_have_attribute(
            "data-state", "ready"
        )

        await ciso_page.get_by_test_id("token-jti").fill(jti)
        await ciso_page.get_by_test_id("token-expiry").fill(expires_at)
        await ciso_page.get_by_test_id("revocation-reason").fill(reason)
        await ciso_page.get_by_test_id("revoke-submit").click()
        await expect(ciso_page.get_by_test_id("revocation-status")).to_have_attribute(
            "data-state", "success"
        )
        await expect(ciso_page.get_by_test_id("revocation-status")).to_contain_text(
            "Token revoked. Audit event:"
        )
        await ciso_context.close()
        await browser.close()

    await _assert_revocation_persisted(jti)
