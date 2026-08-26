from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "frontend/src/main.tsx"
LEGACY = ROOT / "backend/dtmo/unified_console.py"
AUTH = ROOT / "backend/dtmo/auth/dependencies.py"


def test_canonical_workbench_preserves_existing_local_development_identity_context() -> None:
    main = MAIN.read_text(encoding="utf-8")
    legacy = LEGACY.read_text(encoding="utf-8")

    for marker in (
        "sessionStorage.getItem('dtmo.subject') || 'admin-tester'",
        "sessionStorage.getItem('dtmo.roles') || 'admin'",
        "sessionStorage.getItem('dtmo.apiKey') || ''",
        "X-DTMO-Subject",
        "X-DTMO-Roles",
        "X-DTMO-API-Key",
    ):
        assert marker in main

    assert "sessionStorage.getItem('dtmo.subject')||'admin-tester'" in legacy
    assert "sessionStorage.getItem('dtmo.roles')||'admin'" in legacy
    assert "sessionStorage.getItem('dtmo.apiKey')||''" in legacy


def test_canonical_local_auth_bridge_is_same_origin_only_and_does_not_replace_bearer_auth() -> None:
    main = MAIN.read_text(encoding="utf-8")
    auth = AUTH.read_text(encoding="utf-8")

    assert "resolvedUrl.origin !== window.location.origin" in main
    assert "return nativeFetch(input, init)" in main
    assert "if (!headers.has('X-DTMO-Subject'))" in main
    assert "if (!headers.has('X-DTMO-Roles'))" in main
    assert "if (!headers.has('X-DTMO-API-Key'))" in main
    assert "Authorization" not in main

    # Production authorization remains server-side and bearer-token-only.
    assert "if settings.production:" in auth
    assert 'detail="bearer token required"' in auth
    assert "decode_principal_token" in auth
