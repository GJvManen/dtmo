from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from dtmo.api.routes import get_session
from dtmo.audit import AuditDecision
from dtmo.audit.store import append_persistent_audit_event
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal, ROLE_PERMISSIONS, Role
from dtmo.rbac_admin import (
    MANAGED_HUMAN,
    MANAGED_SERVICE_ACCOUNT,
    ManagedPrincipalResponse,
    ManagedPrincipalState,
    ManagedPrincipalStore,
    RbacConflictError,
    RbacValidationError,
    _guard_target,
    _human_admin,
    _response,
)
from dtmo.source_onboarding_experience import _PAGE as SOURCE_ONBOARDING_PAGE

router = APIRouter()


class RolePermissionMatrixResponse(BaseModel):
    roles: list[Role]
    permissions: list[Permission]
    grants: dict[str, dict[str, bool]]
    principal_type_boundary: dict[str, list[Role]]
    separation_of_duties: list[str]
    immutable_policy: bool = True


class GovernedAssignmentRequest(BaseModel):
    display_name: str | None = Field(default=None, max_length=255)
    roles: list[Role] = Field(min_length=1)
    active: bool
    reason: str = Field(min_length=3, max_length=500)


class GovernedAssignmentResponse(BaseModel):
    principal: ManagedPrincipalResponse
    reason: str
    request_id: str
    before: str
    after: str
    authorization_note: str = (
        "Role assignments are constrained by the server-side role catalogue. "
        "Review and external-share approval remain independent governed permissions."
    )


def _state_summary(state: ManagedPrincipalState) -> str:
    roles = ",".join(role.value for role in state.roles)
    display = (state.display_name or "").replace(";", ",")
    return (
        f"subject={state.subject};display_name={display};principal_type={state.principal_type};"
        f"active={str(state.active).lower()};roles={roles}"
    )


def _audit_governed_assignment(
    session: Session,
    *,
    principal: Principal,
    before: ManagedPrincipalState,
    after: ManagedPrincipalState,
    reason: str,
    request_id: str,
) -> None:
    safe_reason = " ".join(reason.strip().split()).replace(";", ",")
    append_persistent_audit_event(
        session,
        principal=principal.subject,
        principal_type="human",
        action="rbac.assignment.update",
        resource=f"principal:{after.subject}",
        decision=AuditDecision.ALLOW,
        request_id=request_id,
        provenance_reference=(
            f"reason:{safe_reason};before:{_state_summary(before)};after:{_state_summary(after)}"
        ),
    )


@router.get(
    "/api/v1/admin/rbac/matrix",
    response_model=RolePermissionMatrixResponse,
    include_in_schema=False,
)
async def role_permission_matrix(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_USERS))],
) -> RolePermissionMatrixResponse:
    _human_admin(principal)
    roles = list(Role)
    permissions = list(Permission)
    grants = {
        role.value: {
            permission.value: permission in ROLE_PERMISSIONS[role]
            for permission in permissions
        }
        for role in roles
    }
    return RolePermissionMatrixResponse(
        roles=roles,
        permissions=permissions,
        grants=grants,
        principal_type_boundary={
            MANAGED_HUMAN: [role for role in roles if role is not Role.SERVICE_ACCOUNT],
            MANAGED_SERVICE_ACCOUNT: [Role.SERVICE_ACCOUNT],
        },
        separation_of_duties=[
            "Service accounts cannot hold human or administrator roles.",
            "Administrators cannot change their own managed assignment.",
            "The last active managed human administrator cannot be removed or deactivated.",
            "Intelligence review and external-share approval remain separately authorized actions.",
            "Role visibility or administration never constitutes review or publication approval.",
        ],
    )


@router.post(
    "/api/v1/admin/rbac/principals/{subject}/governed-assignment",
    response_model=GovernedAssignmentResponse,
    include_in_schema=False,
)
async def update_governed_assignment(
    subject: str,
    request: GovernedAssignmentRequest,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_USERS))],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> GovernedAssignmentResponse:
    _human_admin(principal)
    reason = " ".join(request.reason.strip().split())
    try:
        normalized_subject = _guard_target(principal, subject)

        def mutation(sync: Session) -> tuple[ManagedPrincipalState, ManagedPrincipalState]:
            store = ManagedPrincipalStore(sync)
            before = store.get(normalized_subject)
            if before is None:
                raise RbacConflictError("managed principal not found")
            after = store.update(
                normalized_subject,
                display_name=request.display_name,
                active=request.active,
                roles=request.roles,
                actor=principal.subject,
            )
            _audit_governed_assignment(
                sync,
                principal=principal,
                before=before,
                after=after,
                reason=reason,
                request_id=request_id,
            )
            return before, after

        before, after = await session.run_sync(mutation)
    except RbacConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except RbacValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return GovernedAssignmentResponse(
        principal=_response(after),
        reason=reason,
        request_id=request_id,
        before=_state_summary(before),
        after=_state_summary(after),
    )


_MATRIX_PANEL = r'''
<article class="surface" id="e6-rbac-management" style="grid-column:1/-1;order:-2">
  <div class="page-heading">
    <div>
      <p class="eyebrow">Least privilege & separation of duties</p>
      <h3>Rol- en permissiematrix</h3>
      <p>De matrix komt rechtstreeks uit het server-side autorisatiebeleid. Wijzigingen aan managed assignments vereisen een expliciete reden en worden met actor, correlation/request ID en before/after-state vastgelegd.</p>
    </div>
    <span class="status-pill neutral">Policy-bound</span>
  </div>
  <div id="e6-rbac-status" class="status" role="status" aria-live="polite">Matrix laden…</div>
  <div id="e6-rbac-matrix" class="e6-matrix-wrap"></div>
  <div id="e6-rbac-boundaries" class="cards"></div>
</article>
'''

_CSS = r'''
<style id="e6-rbac-style">
.e6-matrix-wrap{overflow:auto;margin:.75rem 0}.e6-matrix{border-collapse:collapse;width:100%;min-width:900px}.e6-matrix th,.e6-matrix td{border:1px solid var(--line);padding:.45rem;text-align:center;font-size:.78rem}.e6-matrix th:first-child,.e6-matrix td:first-child{text-align:left;position:sticky;left:0;background:var(--surface);z-index:1}.e6-grant{font-weight:800}.e6-no-grant{color:var(--muted)}.e6-reason{display:grid;gap:.3rem;margin-top:.65rem}.e6-reason textarea{min-height:70px;resize:vertical}
</style>
'''

_SCRIPT_TAG = '<script src="/ui/rbac-management-experience.js" defer></script>'


def extend_console_page(page: str) -> str:
    if 'id="e6-rbac-management"' in page:
        return page
    marker = '<article class="surface" id="rbac-administration"'
    if marker not in page:
        raise RuntimeError("canonical RBAC Administration marker not found")
    extended = page.replace(marker, _MATRIX_PANEL + marker, 1)
    extended = extended.replace("</head>", _CSS + "</head>", 1)
    extended = extended.replace("</body>", _SCRIPT_TAG + "</body>", 1)
    return extended


_PAGE = extend_console_page(SOURCE_ONBOARDING_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def rbac_management_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const panel = document.getElementById('e6-rbac-management');
  if (!panel) return;
  const escE6 = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const subject = () => sessionStorage.getItem('dtmo.subject') || 'admin-tester';
  const roles = () => sessionStorage.getItem('dtmo.roles') || 'admin';
  const apiKey = () => sessionStorage.getItem('dtmo.apiKey') || '';
  const requestId = () => globalThis.crypto?.randomUUID?.() || `dtmo-e6-${Date.now()}-${Math.random().toString(16).slice(2)}`;

  async function e6Api(url, options={}) {
    const headers = {'X-DTMO-Subject':subject(),'X-DTMO-Roles':roles(),'X-DTMO-API-Key':apiKey(),...(options.headers||{})};
    if (options.body) headers['Content-Type']='application/json';
    if (options.method && options.method !== 'GET') headers['X-Request-ID']=requestId();
    const response = await fetch(url,{...options,headers});
    let body={}; try { body=await response.json(); } catch (_) { body={}; }
    if (!response.ok) throw new Error(body.detail || `HTTP ${response.status}`);
    return body;
  }

  function renderMatrix(matrix) {
    const permissions = matrix.permissions || [];
    const header = permissions.map((permission) => `<th scope="col">${escE6(permission)}</th>`).join('');
    const rows = (matrix.roles || []).map((role) => `<tr><th scope="row">${escE6(role)}</th>${permissions.map((permission) => matrix.grants?.[role]?.[permission] ? `<td class="e6-grant" aria-label="${escE6(role)} heeft ${escE6(permission)}">✓</td>` : `<td class="e6-no-grant" aria-label="${escE6(role)} heeft niet ${escE6(permission)}">—</td>`).join('')}</tr>`).join('');
    $('e6-rbac-matrix').innerHTML=`<table class="e6-matrix"><thead><tr><th scope="col">Rol</th>${header}</tr></thead><tbody>${rows}</tbody></table>`;
    $('e6-rbac-boundaries').innerHTML=(matrix.separation_of_duties||[]).map((text) => `<article class="card"><strong>Policy boundary</strong><p>${escE6(text)}</p></article>`).join('');
  }

  function upgradePrincipalCards() {
    document.querySelectorAll('[data-rbac-principal]').forEach((card) => {
      if (card.querySelector('[data-e6-reason]')) return;
      const save = card.querySelector('[data-rbac-save]');
      if (!save || save.disabled) return;
      const principalSubject = save.dataset.rbacSave;
      save.removeAttribute('data-rbac-save');
      save.dataset.e6RbacSave=principalSubject;
      save.textContent='Governed opslaan';
      const reason=document.createElement('label');
      reason.className='e6-reason';
      reason.innerHTML='<span>Reden voor wijziging</span><textarea data-e6-reason required minlength="3" maxlength="500" placeholder="Waarom is deze rol- of statuswijziging nodig?"></textarea>';
      save.closest('.actions')?.before(reason);
    });
  }

  function reconcilePrincipalCard(card, principal) {
    if (!card || !principal) return;
    const heading = card.querySelector('.page-heading');
    const badge = heading?.querySelector('.status-pill');
    if (badge) {
      badge.textContent = principal.active ? 'Actief' : 'Inactief';
      badge.classList.toggle('good', Boolean(principal.active));
      badge.classList.toggle('neutral', !principal.active);
    }
    const displayName = card.querySelector('[data-rbac-display-name]');
    if (displayName) displayName.value = principal.display_name || '';
    const active = card.querySelector('[data-rbac-active]');
    if (active) active.checked = Boolean(principal.active);
    const selected = new Set(principal.roles || []);
    card.querySelectorAll('[data-rbac-role]').forEach((input) => {
      input.checked = selected.has(input.dataset.rbacRole);
    });
  }

  async function governedSave(button) {
    const card=button.closest('[data-rbac-principal]');
    if (!card) return;
    const principalSubject=button.dataset.e6RbacSave;
    const result=card.querySelector('[data-rbac-result]');
    const reason=card.querySelector('[data-e6-reason]')?.value.trim() || '';
    if (reason.length < 3) { if(result) result.textContent='Een concrete wijzigingsreden is verplicht.'; return; }
    const payload={display_name:card.querySelector('[data-rbac-display-name]').value.trim()||null,active:card.querySelector('[data-rbac-active]').checked,roles:[...card.querySelectorAll('[data-rbac-role]:checked')].map((node)=>node.dataset.rbacRole),reason};
    if(result) result.textContent='Governed wijziging opslaan…';
    try {
      const response=await e6Api(`/api/v1/admin/rbac/principals/${encodeURIComponent(principalSubject)}/governed-assignment`,{method:'POST',body:JSON.stringify(payload)});
      reconcilePrincipalCard(card,response.principal);
      if(result) result.textContent=`Opgeslagen en geaudit · request ${response.request_id}`;
      card.querySelector('[data-e6-reason]').value='';
    } catch(error) { if(result) result.textContent=`Opslaan mislukt: ${error.message}`; }
  }

  document.getElementById('rbac-principals')?.addEventListener('click',(event)=>{
    const button=event.target.closest('[data-e6-rbac-save]');
    if(button){ event.preventDefault(); event.stopImmediatePropagation(); void governedSave(button); }
  },true);

  const observer=new MutationObserver(upgradePrincipalCards);
  const principals=document.getElementById('rbac-principals');
  if(principals) observer.observe(principals,{childList:true,subtree:true});
  upgradePrincipalCards();
  void e6Api('/api/v1/admin/rbac/matrix').then((matrix)=>{renderMatrix(matrix);$('e6-rbac-status').textContent=`${matrix.roles.length} rollen · ${matrix.permissions.length} permissies · server-side policy.`;}).catch((error)=>{$('e6-rbac-status').textContent=`RBAC-matrix niet beschikbaar: ${error.message}`;});
})();
'''


@router.get("/ui/rbac-management-experience.js", include_in_schema=False)
def rbac_management_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})
