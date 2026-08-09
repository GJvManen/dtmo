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
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DTMO auditor evidence viewer</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 64rem; margin: 2rem auto; padding: 0 1rem; }
    button { padding: .65rem 1rem; font: inherit; }
    #status { margin: 1rem 0; padding: .75rem; border: 1px solid #bbb; }
    #events { display: grid; gap: .75rem; padding: 0; list-style: none; }
    #events li { border: 1px solid #bbb; padding: .75rem; }
    code { overflow-wrap: anywhere; }
  </style>
</head>
<body>
  <main>
    <h1>Read-only audit evidence</h1>
    <p id="auditor-principal" data-testid="auditor-principal">Resolving authenticated principal…</p>
    <section id="audit-panel" data-testid="audit-panel" hidden>
      <p>This surface is read-only. Audit records cannot be changed here.</p>
      <button id="load-audit" data-testid="load-audit" type="button">Load audit evidence</button>
      <div id="audit-status" data-testid="audit-status" role="status" aria-live="polite">Ready to load.</div>
      <ul id="audit-events" data-testid="audit-events"></ul>
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

  function setState(message, state) {
    status.textContent = message;
    status.dataset.state = state;
  }

  async function session() {
    const response = await fetch('/api/v1/ui/session', {credentials: 'same-origin'});
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || `session failed: ${response.status}`);
    principal.textContent = `${body.subject} — roles: ${body.roles.join(', ')}`;
    panel.hidden = !body.permissions.includes('read:audit');
  }

  async function loadAudit() {
    events.replaceChildren();
    setState('Loading audit evidence…', 'loading');
    try {
      const response = await fetch('/api/v1/audit/events?limit=50', {credentials: 'same-origin'});
      let body;
      try { body = await response.json(); } catch (_) { body = {detail: 'invalid response'}; }
      if (!response.ok) throw new Error(body.detail || `audit read failed: ${response.status}`);
      for (const item of body.events || []) {
        const row = document.createElement('li');
        row.dataset.eventId = String(item.event_id);
        const action = document.createElement('strong');
        action.textContent = String(item.action);
        const details = document.createElement('p');
        details.textContent = `${item.principal} — ${item.decision} — ${item.resource}`;
        const hash = document.createElement('code');
        hash.textContent = String(item.event_hash);
        row.append(action, details, hash);
        events.appendChild(row);
      }
      if (body.count === 0) {
        setState('No audit evidence is available.', 'empty');
      } else {
        setState(`${body.count} audit event${body.count === 1 ? '' : 's'} loaded read-only.`, 'success');
      }
    } catch (error) {
      events.replaceChildren();
      setState(`Audit evidence unavailable: ${error.message}`, 'error');
    }
  }

  load.addEventListener('click', () => void loadAudit());
  session().catch((error) => setState(`Session error: ${error.message}`, 'error'));
})();
"""


@router.get("/ui/auditor", response_class=HTMLResponse, include_in_schema=False)
def auditor_page() -> HTMLResponse:
    return HTMLResponse(
        _PAGE,
        headers={
            "Cache-Control": "no-store",
            "Content-Security-Policy": (
                "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                "connect-src 'self'; img-src 'self'; frame-ancestors 'none'"
            ),
        },
    )


@router.get("/ui/auditor.js", include_in_schema=False)
def auditor_script() -> Response:
    return Response(
        _SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )


@router.get("/api/v1/audit/events")
async def read_audit_events(
    principal: Annotated[
        Principal,
        Depends(require_permission(Permission.READ_AUDIT)),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, object]:
    del principal
    records = (
        await session.scalars(
            select(AuditEventRecord)
            .order_by(AuditEventRecord.sequence_number.desc())
            .limit(limit)
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
