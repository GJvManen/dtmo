from __future__ import annotations

from dtmo.frontend import console_css, console_page, console_script


def test_console_is_published_at_root_with_security_headers() -> None:
    response = console_page()
    body = response.body.decode("utf-8")

    assert response.status_code == 200
    assert "Threat Operations Console" in body
    assert "Intelligence explorer" in body
    assert "Governed decision workspace" in body
    assert "Audit evidence" in body
    assert "CISO controls" in body
    assert "Separation of duties" in body
    assert "External share approval" in body
    assert response.headers["cache-control"] == "no-store"
    csp = response.headers["content-security-policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    assert "base-uri 'none'" in csp
    assert "form-action 'self'" in csp


def test_console_information_architecture_is_discoverable() -> None:
    body = console_page().body.decode("utf-8")

    for section in ("overview", "intelligence", "governance", "audit", "security"):
        assert f'id="{section}"' in body
        assert f'data-section-link="{section}"' in body
    assert 'href="/ui/analyst-search"' in body
    assert 'href="/ui/share-approval"' in body
    assert 'href="/ui/auditor"' in body
    assert 'href="/ui/ciso-security"' in body
    assert 'id="identity-dialog"' in body


def test_console_assets_preserve_accessibility_and_governance_contract() -> None:
    css = console_css().body.decode("utf-8")
    script = console_script().body.decode("utf-8")

    assert ":focus-visible" in css
    assert "prefers-reduced-motion" in css
    assert ".sr-only" in css
    assert ".skip-link" in css
    assert "sessionStorage" in script
    assert "localStorage" not in script
    assert "X-DTMO-API-Key" in script
    assert "review:intelligence" in script
    assert "approve:share" in script
    assert "read:audit" in script
    assert "revoke:tokens" in script
    assert "crypto.randomUUID()" in script
    assert "IntersectionObserver" in script


def test_console_does_not_persist_or_embed_credentials() -> None:
    page = console_page().body.decode("utf-8")
    script = console_script().body.decode("utf-8")

    assert "Bearer " not in page
    assert "Authorization" not in page
    assert "localStorage" not in page + script
    assert "change-me" not in page
