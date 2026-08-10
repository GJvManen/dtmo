from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.persistence.audit_models import AuditEventRecord

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DTMO — Auditor evidence</title>
  <link rel="stylesheet" href="/ui/design-system.css">
</head>
<body>
  <a class="skip-link" href="#main">Ga naar hoofdinhoud</a>
  <header class="app-header">
    <div><p class="eyebrow">Auditor workspace</p><h1>Read-only audit evidence</h1></div>
    <div class="header-actions"><a class="button ghost" href="/">Terug naar console</a><span id="auditor-principal" data-testid="auditor-principal" class="status-pill neutral" role="status" aria-live="polite">Principal bepalen…</span></div>
  </header>
  <main id="main" class="workspace">
    <section class="page-heading"><div><p class="eyebrow">Auditability</p><h2>Evidence viewer</h2><p>Bekijk recente audit-events zonder wijzigingsmogelijkheden. Event hashes, principals, decisions en resources blijven zichtbaar voor onafhankelijke controle.</p></div></section>
    <section id="audit-panel" data-testid="audit-panel" class="surface table-surface" hidden>
      <div class="surface-header" style="padding:1rem 1rem 0"><div><p class="eyebrow">Append-only evidence</p><h3>Recente audit events</h3></div><button id="load-audit" data-testid="load-audit" class="button secondary" type="button">Evidence laden</button></div>
      <div id="audit-status" data-testid="audit-status" class="inline-status" role="status" aria-live="polite">Klaar om evidence te laden.</div>
      <div class="table-wrap"><table><thead><tr><th scope="col">Actie</th><th scope="col">Principal</th><th scope="col">Decision</th><th scope="col">Resource</th><th scope="col">Event hash</th></tr></thead><tbody id="audit-events" data-testid="audit-events"><tr><td colspan="5" class="empty-cell">Nog geen audit evidence geladen.</td></tr></tbody></table></div>
    </section>
  </main>
  <script src="/ui/auditor.js" defer></script>
</body>
</html>
"""

_SCRIPT = r"""(() => {
  const principal = document.getElementById('auditor-principal');
  const panel = document.getElementById('audit-panel');
  const load = document.getElementById('load-audit');
  const status = document.getElementById('audit-status');
  const events = document.getElementById('audit-events');
  function setState(message, state) { status.textContent = message; status.dataset.state = state; }
  async function session() {
    const response = await fetch('/api/v1/ui/session', {credentials:'same-origin'}); const body = await response.json();
    if (!response.ok) throw new Error(body.detail || `session failed: ${response.status}`);
    principal.textContent = `${body.subject} · ${body.roles.join(', ') || 'geen rollen'}`; principal.className = 'status-pill success';
    panel.hidden = !body.permissions.includes('read:audit');
    if (panel.hidden) setState('Audit evidence is niet toegestaan voor deze principal.', 'error');
  }
  async function loadAudit() {
    events.innerHTML = '<tr><td colspan="5" class="empty-cell">Audit evidence laden…</td></tr>'; setState('Audit evidence laden…','loading');
    try {
      const response = await fetch('/api/v1/audit/events?limit=50',{credentials:'same-origin'}); let body;
      try { body = await response.json(); } catch (_) { body = {detail:'invalid response'}; }
      if (!response.ok) throw new Error(body.detail || `audit read failed: ${response.status}`);
      events.replaceChildren();
      for (const item of body.events || []) {
        const row = document.createElement('tr');
        for (const value of [item.action,item.principal,item.decision,item.resource]) { const cell=document.createElement('td'); cell.textContent=String(value||'—'); row.appendChild(cell); }
        const hashCell=document.createElement('td'); const code=document.createElement('code'); code.textContent=String(item.event_hash||'—'); hashCell.appendChild(code); row.appendChild(hashCell); events.appendChild(row);
      }
      if (!body.count) events.innerHTML='<tr><td colspan="5" class="empty-cell">Geen audit evidence beschikbaar.</td></tr>';
      setState(`${body.count || 0} audit event${body.count === 1 ? '' : 's'} geladen (read-only).`,'success');
    } catch (error) { events.innerHTML='<tr><td colspan="5" class="empty-cell">Audit evidence niet beschikbaar.</td></tr>'; setState(`Audit evidence niet beschikbaar: ${error.message}`,'error'); }
  }
  load.addEventListener('click',()=>void loadAudit());
  session().catch((error)=>{principal.textContent=`Sessiefout: ${error.message}`;principal.className='status-pill error';setState('Geen geautoriseerde sessie.','error');});
})();
"""


def _page_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-store",
        "Content-Security-Policy": (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; "
            "img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        ),
    }


@router.get("/ui/auditor", response_class=HTMLResponse, include_in_schema=False)
def auditor_page() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers=_page_headers())


@router.get("/ui/auditor.js", include_in_schema=False)
def auditor_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})


@router.get("/api/v1/audit/events")
async def read_audit_events(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_AUDIT))],
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, object]:
    del principal
    records = (
        await session.scalars(
            select(AuditEventRecord).order_by(AuditEventRecord.sequence_number.desc()).limit(limit)
        )
    ).all()
    return {
        "count": len(records),
        "read_only": True,
        "events": [
            {
                "sequence_number": record.sequence_number,
                "event_id": str(record.event_id),
                "occurred_at": record.occurred_at.isoformat(),
                "principal": record.principal,
                "principal_type": record.principal_type,
                "action": record.action,
                "resource": record.resource,
                "decision": record.decision,
                "request_id": record.request_id,
                "provenance_reference": record.provenance_reference,
                "previous_hash": record.previous_hash,
                "event_hash": record.event_hash,
                "schema_version": record.schema_version,
            }
            for record in records
        ],
    }
