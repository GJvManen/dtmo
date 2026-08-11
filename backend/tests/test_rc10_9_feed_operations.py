from __future__ import annotations

from dtmo.source_center import source_center


def test_source_center_exposes_framework_feed_operations() -> None:
    body = source_center().body.decode("utf-8")

    assert "RC10.9 feed operations" in body
    assert "Registreer ondersteunde feeds" in body
    assert "Feed nu laden" in body
    assert "Inschakelen" in body
    assert "/api/v1/source-center/status" in body
    assert "/api/v1/admin/sources/catalog/bootstrap" in body
    assert "/api/v1/admin/sources/" in body
    assert "/connectors/" in body


def test_source_center_preserves_governance_and_request_identity() -> None:
    body = source_center().body.decode("utf-8")

    assert "manage:connectors" in body
    assert "review en externe share approval" in body
    assert "X-DTMO-Subject" in body
    assert "X-DTMO-Roles" in body
    assert "X-DTMO-API-Key" in body
    assert "X-Request-ID" in body
    assert "crypto.randomUUID()" in body
    assert "localStorage" not in body


def test_source_center_has_accessible_live_run_feedback() -> None:
    body = source_center().body.decode("utf-8")

    assert 'role="status"' in body
    assert 'aria-live="polite"' in body
    assert 'aria-labelledby="feed-heading"' in body
    assert 'aria-label="Feed summary"' in body
    assert "Feedrun gestart" in body
    assert "Run geblokkeerd/mislukt" in body
