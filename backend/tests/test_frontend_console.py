from __future__ import annotations

from dtmo.frontend import console_alias, console_css, console_page, console_script


def test_console_is_published_at_root_with_security_headers() -> None:
    response = console_page()
    body = response.body.decode("utf-8")

    assert response.status_code == 200
    assert "DTMO Console" in body
    assert "Intelligence zoeken" in body
    assert "Review & share decision" in body
    assert "Read-only audit evidence" in body
    assert "CISO token revocation" in body
    assert "RBAC · provenance · privacy · auditability · human share approval" in body
    assert response.headers["cache-control"] == "no-store"
    csp = response.headers["content-security-policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    assert "base-uri 'none'" in csp


def test_console_alias_matches_root_surface() -> None:
    assert console_alias().body == console_page().body


def test_console_assets_preserve_accessibility_and_governance_contract() -> None:
    css = console_css().body.decode("utf-8")
    script = console_script().body.decode("utf-8")

    assert ":focus-visible" in css
    assert "prefers-reduced-motion" in css
    assert ".sr-only" in css
    assert "sessionStorage" in script
    assert "localStorage" not in script
    assert "X-DTMO-API-Key" in script
    assert "review:intelligence" in script
    assert "approve:share" in script
    assert "read:audit" in script
    assert "revoke:tokens" in script
    assert "crypto.randomUUID()" in script
