from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DTMO — Administration Center</title><link rel="stylesheet" href="/ui/design-system.css">
</head>
<body><a class="skip-link" href="#content">Ga naar hoofdinhoud</a>
<main id="content" class="workspace">
<header class="page-heading"><div><p class="eyebrow">RC10.5 administration consolidation</p><h1>Administration Center</h1><p>Één navigatiepunt voor bestaande beheeroppervlakken, zonder hun autorisatiegrenzen samen te voegen.</p></div><a class="button ghost" href="/ui/operations">Operations</a></header>
<section class="content-grid equal" aria-label="Beheergebieden">
<article class="surface"><p class="eyebrow">Sources</p><h2>Source administration</h2><p>Registrywijzigingen, bronvalidatie en handmatige runs blijven beschermd door de bestaande menselijke admin + <code>manage:connectors</code> control plane.</p><div class="header-actions"><a class="button primary" href="/ui/admin-sources">Bronconfiguratie</a><a class="button secondary" href="/ui/source-center">Source status</a></div></article>
<article class="surface"><p class="eyebrow">Security</p><h2>Security administration</h2><p>Token revocation blijft een afzonderlijke privileged CISO-actie met de bestaande expliciete revoke-permissie en auditregistratie.</p><a class="button danger" href="/ui/ciso-security">Security controls</a></article>
<article class="surface"><p class="eyebrow">Governance</p><h2>Review & share approval</h2><p>Human review en externe share approval blijven afzonderlijke beslissingen. Deze administration hub verleent geen van beide rechten.</p><a class="button secondary" href="/ui/share-approval">Share approval workspace</a></article>
<article class="surface"><p class="eyebrow">Assurance</p><h2>Audit</h2><p>Audit blijft read-only en gescheiden van operationele of security mutations.</p><a class="button secondary" href="/ui/auditor">Audit workspace</a></article>
</section>
<section class="surface"><h2>Separation-of-duties boundary</h2><p>Dit scherm consolideert uitsluitend navigatie en uitleg. Het voegt geen API-endpoint voor mutations toe, omzeilt geen server-side RBAC en combineert geen source-, security-, review-, share-approval- of auditautoriteit.</p></section>
</main></body></html>"""


@router.get("/ui/administration", response_class=HTMLResponse)
def administration_center() -> HTMLResponse:
    return HTMLResponse(_PAGE)
