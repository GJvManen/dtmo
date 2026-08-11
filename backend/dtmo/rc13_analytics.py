from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from dtmo.frontend import _CSS as BASE_DESIGN_SYSTEM_CSS

router = APIRouter()

# RC13.2 deliberately keeps Grafana authenticated and available to deployment
# operators, but removes the separately authenticated embed from the canonical
# end-user console. Native DTMO analytics remain the product surface until a
# future deployment can prove a shared authentication boundary without
# anonymous access or privilege broadening.
_SINGLE_SESSION_ANALYTICS_CSS = (
    BASE_DESIGN_SYSTEM_CSS
    + "\n/* RC13.2 single-session analytics */\n"
    + ".grafana-shell{display:none!important}\n"
)


@router.get("/ui/design-system.css", include_in_schema=False)
@router.get("/ui/console.css", include_in_schema=False)
def single_session_design_system() -> Response:
    return Response(
        _SINGLE_SESSION_ANALYTICS_CSS,
        media_type="text/css",
        headers={"Cache-Control": "no-store"},
    )
