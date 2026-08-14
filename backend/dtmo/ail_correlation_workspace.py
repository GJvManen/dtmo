from __future__ import annotations

import json
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, Response
from minio.error import S3Error
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.ail_correlation import correlate_ail_indicator
from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.lake.minio_store import MinioObjectStore
from dtmo.persistence.models import IntelligenceItem
from dtmo.threat_workspace import _PAGE as BASE_PAGE, router as threat_workspace_router

router = APIRouter()
_store = MinioObjectStore()


def _enum_value(value: object) -> str:
    return str(getattr(value, "value", value))


def _indicator_from_external_id(external_id: str | None) -> tuple[str, str]:
    if not external_id:
        raise ValueError("AIL item has no external id")
    parts = external_id.split(":", 2)
    if len(parts) != 3 or not parts[0].strip() or not parts[2].strip():
        raise ValueError("AIL external id is not a supported global object id")
    return parts[0].strip(), parts[2].strip()


async def _read_raw_projection(item: IntelligenceItem) -> dict[str, Any] | None:
    raw_object = item.metadata_json.get("raw_object")
    if not isinstance(raw_object, dict):
        return None
    bucket = raw_object.get("bucket")
    key = raw_object.get("key")
    if not isinstance(bucket, str) or not isinstance(key, str):
        return None
    payload = await _store.get_bytes(bucket, key)
    decoded = json.loads(payload)
    return decoded if isinstance(decoded, dict) else None


def _candidate_projection(item: IntelligenceItem, raw: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "source_id": item.source_id,
        "external_id": item.external_id,
        "item_type": _enum_value(item.item_type),
        "title": item.title,
        "summary": item.summary,
        "tags": list(item.tags),
        "metadata": dict(item.metadata_json),
        "raw": raw or {},
    }


def _investigation_refs(raw: dict[str, Any] | None) -> list[dict[str, str]]:
    if not isinstance(raw, dict):
        return []
    projection = raw.get("_dtmo_ail")
    if not isinstance(projection, dict):
        return []
    refs = projection.get("investigation_references")
    if not isinstance(refs, list):
        return []
    result: list[dict[str, str]] = []
    for ref in refs:
        if isinstance(ref, dict) and isinstance(ref.get("id"), str) and ref["id"].strip():
            result.append({"id": ref["id"].strip()})
    return result


@router.get("/api/v1/intelligence/{item_id}/ail-correlations")
async def ail_workspace_correlations(
    item_id: UUID,
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    del principal
    source = await session.get(IntelligenceItem, item_id)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="intelligence item not found")
    if source.source_id != "ail":
        return {"status": "empty", "reason": "correlation experience is scoped to AIL-derived indicators", "correlations": [], "investigation_references": [], "raw_content_exposed": False, "analysis_only": True}

    try:
        indicator_type, indicator_value = _indicator_from_external_id(source.external_id)
    except ValueError as exc:
        return {"status": "degraded", "reason": str(exc), "correlations": [], "investigation_references": [], "raw_content_exposed": False, "analysis_only": True}

    degraded_reasons: list[str] = []
    source_raw: dict[str, Any] | None = None
    try:
        source_raw = await _read_raw_projection(source)
    except (S3Error, OSError, ValueError, json.JSONDecodeError) as exc:
        degraded_reasons.append(f"AIL provenance projection unavailable: {type(exc).__name__}")

    candidates = list((await session.scalars(select(IntelligenceItem).where(IntelligenceItem.id != source.id).order_by(IntelligenceItem.discovered_at.desc()).limit(500))).all())
    projected: list[dict[str, Any]] = []
    for candidate in candidates:
        raw: dict[str, Any] | None = None
        if candidate.source_id == "misp":
            try:
                raw = await _read_raw_projection(candidate)
            except (S3Error, OSError, ValueError, json.JSONDecodeError) as exc:
                degraded_reasons.append(f"MISP projection unavailable for {candidate.external_id or candidate.id}: {type(exc).__name__}")
        projected.append(_candidate_projection(candidate, raw))

    hits = correlate_ail_indicator(indicator_type=indicator_type, indicator_value=indicator_value, candidates=projected)
    correlations = [{"source_id": hit.source_id, "external_id": hit.external_id, "item_type": hit.item_type, "title": hit.title, "relation": hit.relation, "matched_value": hit.matched_value, "context": hit.context} for hit in hits]
    state = "degraded" if degraded_reasons else ("ok" if correlations else "empty")
    return {
        "status": state,
        "indicator": {"type": indicator_type, "value": indicator_value},
        "investigation_references": _investigation_refs(source_raw),
        "correlations": correlations,
        "degraded_reasons": degraded_reasons,
        "raw_content_exposed": False,
        "analysis_only": True,
        "claim_boundary": "Exact correlation is analytical context only; it does not prove exposure, compromise, attribution or share authority.",
    }


_PANEL = """<section id=\"ail-correlation-panel\" class=\"ti-correlation surface\" aria-live=\"polite\"><div class=\"surface-header\"><div><p class=\"eyebrow\">E8.9 AIL correlation</p><h3>Investigation correlations</h3></div><span id=\"ail-correlation-status\" class=\"status-pill neutral\">Selecteer AIL intelligence</span></div><div id=\"ail-correlation-content\"><p class=\"muted\">Voor AIL-derived indicators worden exact-match correlaties met DTMO, MISP en vulnerability-context getoond. Raw leak-content wordt niet weergegeven.</p></div></section>"""
_PAGE = BASE_PAGE.replace(
    '<link rel="stylesheet" href="/ui/design-system.css"><link rel="stylesheet" href="/ui/threat-workspace.css">',
    '<link rel="stylesheet" href="/ui/design-system.css"><link rel="stylesheet" href="/ui/threat-workspace.css"><link rel="stylesheet" href="/ui/ail-correlation-workspace.css">',
).replace(
    '<div id="detail"><p class="muted">Selecteer een resultaat om context en provenance te bekijken.</p></div></article>',
    '<div id="detail"><p class="muted">Selecteer een resultaat om context en provenance te bekijken.</p></div>' + _PANEL + '</article>',
).replace(
    '<script src="/ui/threat-workspace.js" defer></script></body>',
    '<script src="/ui/threat-workspace.js" defer></script><script src="/ui/ail-correlation-workspace.js" defer></script></body>',
)

_JS = r"""
(()=>{
const esc=(value)=>String(value??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
const panel=document.getElementById('ail-correlation-content');
const badge=document.getElementById('ail-correlation-status');
if(!panel||!badge||typeof window.loadDetail!=='function')return;
const original=window.loadDetail;
window.loadDetail=async function(id){
  await original(id);
  badge.textContent='Correlaties laden…'; badge.className='status-pill neutral'; panel.innerHTML='<p class="muted">Correlaties laden…</p>';
  try{
    const data=await api(`/api/v1/intelligence/${encodeURIComponent(id)}/ail-correlations`);
    badge.textContent=data.status==='ok'?`${data.correlations.length} correlaties`:data.status==='degraded'?'Degraded':'Geen correlaties';
    badge.className=`status-pill ${data.status==='ok'?'good':data.status==='degraded'?'warning':'neutral'}`;
    if(data.status==='empty'){panel.innerHTML=`<p class="muted">${esc(data.reason||'Geen exacte correlaties gevonden.')}</p>`;return;}
    const refs=(data.investigation_references||[]).map(r=>`<span class="ti-correlation-ref">${esc(r.id)}</span>`).join('')||'<span class="muted">Geen investigation-referenties</span>';
    const hits=(data.correlations||[]).map(hit=>`<article class="ti-correlation-hit" data-relation="${esc(hit.relation)}"><strong>${esc(hit.title)}</strong><div class="ti-meta"><span>${esc(hit.source_id)}</span><span>${esc(hit.item_type)}</span><span>${esc(hit.relation)}</span></div><p>Exact match: <code>${esc(hit.matched_value)}</code></p>${hit.context?.cve_id?`<p>CVE: ${esc(hit.context.cve_id)} · ${esc(hit.context.vendor||'—')} / ${esc(hit.context.product||'—')}</p>`:''}${hit.context?.object_name?`<p>MISP object: ${esc(hit.context.object_name)} · ${esc(hit.context.type||'')}</p>`:''}</article>`).join('')||'<p class="muted">Geen exacte correlaties gevonden.</p>';
    const degraded=(data.degraded_reasons||[]).length?`<div class="inline-status" role="status"><strong>Degraded evidence:</strong> ${(data.degraded_reasons||[]).map(esc).join('; ')}</div>`:'';
    panel.innerHTML=`<p><strong>Indicator:</strong> ${esc(data.indicator?.type)} · <code>${esc(data.indicator?.value)}</code></p><div class="ti-meta">${refs}</div>${degraded}<div class="ti-correlation-list">${hits}</div><p class="muted">${esc(data.claim_boundary||'Analytical context only.')}</p>`;
  }catch(err){badge.textContent='Degraded';badge.className='status-pill warning';panel.innerHTML=`<div class="inline-status" role="status">Correlatie-evidence niet beschikbaar: ${esc(err.message)}</div>`;}
};
})();
"""

_CSS = ".ti-correlation{margin-top:1rem;padding:1rem;background:#091725;border:1px solid #20384f}.ti-correlation-list{display:grid;gap:.65rem;margin-top:.75rem}.ti-correlation-hit{border-left:3px solid #2d648d;padding:.75rem;background:#0a1724}.ti-correlation-hit p{margin:.45rem 0;color:#b9c8d8}.ti-correlation-ref{padding:.2rem .45rem;border:1px solid #24425d;border-radius:999px;color:#cbd8e5}.status-pill.warning{border-color:#b97416;color:#ffd79b}"


@router.get("/ui/intelligence-workspace", response_class=HTMLResponse)
def ail_enhanced_intelligence_workspace() -> HTMLResponse:
    return HTMLResponse(_PAGE)


@router.get("/ui/ail-correlation-workspace.js")
def ail_correlation_workspace_js() -> Response:
    return Response(_JS, media_type="application/javascript")


@router.get("/ui/ail-correlation-workspace.css")
def ail_correlation_workspace_css() -> Response:
    return Response(_CSS, media_type="text/css")


# Main already mounts the canonical threat-workspace router. E8.9b is loaded by
# the AIL connector module and prepends these bounded routes so the enhanced UI
# wins the duplicate GET path without replacing any pre-existing RC10.3 routes.
for _route in reversed(router.routes):
    threat_workspace_router.routes.insert(0, _route)
