from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from dtmo.post_rc13_severity import _SCRIPT as BASE_SEVERITY_SCRIPT

router = APIRouter()

# The accepted RC13 browser lifecycle owns the initial `all severities` status.
# Only a persisted non-default user preference needs an automatic filtered
# refresh after page load. Explicit user changes are still handled by the base
# severity script's change listener.
_SCRIPT = BASE_SEVERITY_SCRIPT.replace(
    "  syncControls();\n  void applySeverity(selected);",
    "  syncControls();\n  if (selected !== 'all') void applySeverity(selected);",
)

if _SCRIPT == BASE_SEVERITY_SCRIPT:
    raise RuntimeError("post-RC13 severity bootstrap marker not found")


@router.get("/ui/post-rc13-severity.js", include_in_schema=False)
def post_rc13_severity_script() -> Response:
    return Response(
        _SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )
