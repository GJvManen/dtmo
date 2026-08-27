from __future__ import annotations

import os
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from playwright.async_api import async_playwright, expect
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from dtmo.connectors.state import ConnectorHealthEvent, ConnectorRuntimeState

BASE_URL = os.environ.get("DTMO_E2E_BASE_URL", "")
DATABASE_URL = os.environ.get("DTMO_DATABASE_URL", "")
pytestmark = pytest.mark.skipif(
    not BASE_URL or not DATABASE_URL,
    reason="Operations functional recovery executes only in the dedicated exact-head browser workflow",
)


@pytest.mark.asyncio
async def test_operations_exposes_persisted_connector_runtime_evidence_without_mutation_authority() -> None:
    suffix = uuid4().hex[:8]
    connector_id = f"operations-recovery-{suffix}"
    run_id = uuid4()
    observed_at = datetime.now(UTC)
    engine = create_async_engine(DATABASE_URL)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        session.add(
            ConnectorRuntimeState(
                connector_id=connector_id,
                last_run_id=run_id,
                last_success_at=observed_at,
                consecutive_failures=0,
                health_status="healthy",
                updated_at=observed_at,
            )
        )
        await session.flush()
        session.add(
            ConnectorHealthEvent(
                connector_id=connector_id,
                run_id=run_id,
                observed_at=observed_at,
                status="success",
                duration_seconds=1.25,
                record_count=2,
                quarantine_count=1,
                publish_approved=False,
            )
        )
        await session.commit()

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                extra_http_headers={
                    "X-DTMO-Subject": "functional-recovery-operations-human",
                    "X-DTMO-Roles": "auditor",
                }
            )
            page = await context.new_page()
            await page.goto(f"{BASE_URL}/workbench/operations")

            await expect(page.get_by_role("heading", name="Operations", exact=True)).to_be_visible()
            runtime = page.locator('[data-operations-section="connector-runtime-evidence"]')
            await expect(runtime).to_contain_text("dtmo-persistent-connector-runtime-state")
            connector = page.locator(f'[data-connector-runtime="{connector_id}"]')
            await expect(connector).to_contain_text(connector_id)
            await expect(connector).to_contain_text("healthy")
            await expect(connector).to_contain_text(str(run_id))

            runs = page.locator('[data-operations-section="recent-connector-runs"]')
            await expect(runs).to_contain_text(connector_id)
            await expect(runs).to_contain_text("2 records")
            await expect(runs).to_contain_text("1 quarantined")
            await expect(runs).to_contain_text("publication approved: no")
            await expect(runtime).to_contain_text("operational evidence only")
            assert await page.locator('a[href^="/ui/"]').count() == 0

            await context.close()
            await browser.close()
    finally:
        async with session_factory() as session:
            await session.execute(delete(ConnectorHealthEvent).where(ConnectorHealthEvent.connector_id == connector_id))
            await session.execute(delete(ConnectorRuntimeState).where(ConnectorRuntimeState.connector_id == connector_id))
            await session.commit()
        await engine.dispose()
