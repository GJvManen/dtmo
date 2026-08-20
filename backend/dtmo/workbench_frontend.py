from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse, Response

router = APIRouter()


def _dist_root() -> Path:
    configured = os.environ.get("DTMO_FRONTEND_DIST", "frontend/dist")
    return Path(configured).expanduser().resolve()


def _index_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store",
        "Content-Security-Policy": (
            "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
            "img-src 'self' data:; font-src 'self'; frame-ancestors 'none'; base-uri 'none'; "
            "form-action 'self'; object-src 'none'"
        ),
        "X-DTMO-Frontend-Mode": "canonical-workbench",
    }


def _serve_index() -> Response:
    index = _dist_root() / "index.html"
    if not index.is_file():
        return RedirectResponse(
            url="/ui/console",
            status_code=307,
            headers={
                "Cache-Control": "no-store",
                "X-DTMO-Frontend-Mode": "compatibility-fallback",
            },
        )
    return FileResponse(index, media_type="text/html", headers=_index_headers())


@router.get("/", include_in_schema=False)
def canonical_root() -> RedirectResponse:
    """Declare the built workbench as the canonical browser route."""
    return RedirectResponse(url="/workbench/", status_code=307, headers={"Cache-Control": "no-store"})


@router.get("/workbench", include_in_schema=False)
def workbench_without_slash() -> RedirectResponse:
    return RedirectResponse(url="/workbench/", status_code=307, headers={"Cache-Control": "no-store"})


@router.get("/workbench/assets/{asset_path:path}", include_in_schema=False)
def workbench_asset(asset_path: str) -> FileResponse:
    assets = (_dist_root() / "assets").resolve()
    candidate = (assets / asset_path).resolve()
    if not candidate.is_relative_to(assets) or not candidate.is_file():
        raise HTTPException(status_code=404, detail="workbench asset not found")
    return FileResponse(
        candidate,
        headers={
            "Cache-Control": "public, max-age=31536000, immutable",
            "X-DTMO-Frontend-Mode": "canonical-workbench",
        },
    )


@router.get("/workbench/", include_in_schema=False)
def workbench_index() -> Response:
    return _serve_index()


@router.get("/workbench/{client_path:path}", include_in_schema=False)
def workbench_client_route(client_path: str) -> Response:
    del client_path
    return _serve_index()
