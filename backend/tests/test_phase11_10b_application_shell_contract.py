from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_canonical_frontend_stack_is_exactly_pinned_and_locked() -> None:
    package = json.loads(read("frontend/package.json"))
    lock = json.loads(read("frontend/package-lock.json"))
    assert package["private"] is True
    assert package["scripts"]["build"] == "tsc --noEmit && vite build"
    expected = {
        "react",
        "react-dom",
        "react-router-dom",
        "@tanstack/react-query",
    }
    assert expected <= set(package["dependencies"])
    assert {"typescript", "vite", "@vitejs/plugin-react"} <= set(package["devDependencies"])
    for section in ("dependencies", "devDependencies"):
        for version in package[section].values():
            assert version[0].isdigit(), f"dependency must be exact-pinned: {version}"
            assert not version.startswith(("^", "~", ">", "<", "*"))

    assert lock["lockfileVersion"] == 3
    root = lock["packages"][""]
    assert root["dependencies"] == package["dependencies"]
    assert root["devDependencies"] == package["devDependencies"]
    assert lock["packages"]["node_modules/react"]["version"] == package["dependencies"]["react"]
    assert lock["packages"]["node_modules/react-router-dom"]["version"] == package["dependencies"]["react-router-dom"]
    assert lock["packages"]["node_modules/@tanstack/react-query"]["version"] == package["dependencies"]["@tanstack/react-query"]


def test_supported_build_consumes_committed_lockfile_without_regeneration() -> None:
    dockerfile = read("Dockerfile")
    workflow = read(".github/workflows/phase11-application-shell.yml")
    assert "COPY frontend/package.json frontend/package-lock.json ./" in dockerfile
    assert "RUN npm ci" in dockerfile
    assert "npm install --package-lock-only" not in dockerfile
    assert "cache-dependency-path: frontend/package-lock.json" in workflow
    assert "npm ci" in workflow
    assert "Bootstrap lockfile" not in workflow
    assert "npm install --package-lock-only" not in workflow
    assert "git diff --exit-code -- frontend/package.json frontend/package-lock.json" in workflow


def test_workbench_is_a_real_react_router_shell() -> None:
    main = read("frontend/src/main.tsx")
    app = read("frontend/src/App.tsx")
    styles = read("frontend/src/styles.css")
    for marker in ("QueryClientProvider", "BrowserRouter", 'basename="/workbench"'):
        assert marker in main
    for marker in (
        "Command Center",
        "Threat Intelligence",
        "Exposure",
        "Investigations",
        "Analysis & Enrichment",
        "Sharing & Exchange",
        "Automation & Playbooks",
        "Collection",
        "Governance & Evidence",
        "Operations",
        "Administration",
        "Command palette",
        "Object details",
        "Geen object geselecteerd",
        "No synthetic operational state",
        "/api/v1/ui/session",
        "/health",
        "/ui/console",
    ):
        assert marker in app
    for marker in (
        "--bg:",
        "--surface:",
        "--text:",
        "--accent:",
        "--success:",
        "--warning:",
        "--error:",
        "--focus:",
        ".skip-link",
        "prefers-reduced-motion",
        "@media(max-width:900px)",
    ):
        assert marker in styles


def test_browser_does_not_become_an_upstream_integration_client() -> None:
    source = "\n".join(
        read(path)
        for path in (
            "frontend/src/main.tsx",
            "frontend/src/App.tsx",
        )
    ).lower()
    for forbidden in (
        "taranis.ai",
        "intelowl",
        "opencti",
        "misp.local",
        "thehive",
        "cortex.local",
        "localhost:9001",
    ):
        assert f"http://{forbidden}" not in source
        assert f"https://{forbidden}" not in source
    assert "fetch('/api/v1/ui/session'" in source or "fetchjson<session>('/api/v1/ui/session'" in source


def test_backend_serves_built_shell_and_fails_to_legacy_only_when_dist_is_absent() -> None:
    serving = read("backend/dtmo/workbench_frontend.py")
    main = read("backend/dtmo/main.py")
    for marker in (
        "DTMO_FRONTEND_DIST",
        'url="/workbench/"',
        'url="/ui/console"',
        '"X-DTMO-Frontend-Mode": "canonical-workbench"',
        "is_relative_to",
        "max-age=31536000, immutable",
        "Content-Security-Policy",
        "object-src 'none'",
    ):
        assert marker in serving
    assert "from dtmo.workbench_frontend import router as workbench_frontend_router" in main
    assert main.index("app.include_router(workbench_frontend_router)") < main.index("app.include_router(unified_console_router)")


def test_vite_build_is_csp_compatible_and_does_not_publish_source_maps() -> None:
    config = read("frontend/vite.config.ts")
    index = read("frontend/index.html")
    assert "base: '/workbench/'" in config
    assert "sourcemap: false" in config
    assert "manifest: true" in config
    assert "assetsDir: 'assets'" in config
    assert '<div id="root"></div>' in index
    assert "http://" not in index
    assert "https://" not in index


def test_phase11_10b_scope_remains_shell_only() -> None:
    app = read("frontend/src/App.tsx")
    assert "11.10b shell foundation" in app
    assert "Functional command-center content is delivered in Phase 11.10c." in app
    assert "Feature data appears only when its governed DTMO API contract is implemented" in app
    assert "Publication/share authority remains server-side and human-governed." in app
