from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

from dtmo.framework_experience import _PAGE as FRAMEWORK_PAGE

router = APIRouter()

_PANEL = r'''
<article class="surface governance-crosswalk" id="governance-crosswalk" style="margin-top:1rem">
  <div class="page-heading">
    <div>
      <p class="eyebrow">Repository-backed control crosswalk</p>
      <h3>Uitgewerkte kaders & expliciete DTMO-mappings</h3>
      <p>Concrete DTMO-controls gekoppeld aan Normenkader IBP, MITRE ATT&amp;CK, NIST CSF en CVSS-context. Elke relatie heeft een type, rationale, implementatiebewijs en authoritative bron.</p>
    </div>
    <button id="crosswalk-refresh" class="button secondary" type="button">Mappings vernieuwen</button>
  </div>
  <div id="crosswalk-status" class="status" role="status" aria-live="polite">Expliciete mappings laden…</div>
  <div id="crosswalk-summary" class="framework-summary" aria-label="Crosswalkstatistieken"></div>
  <div class="framework-table-wrap">
    <table id="crosswalk-table" aria-label="DTMO framework crosswalk">
      <thead><tr><th>DTMO-control</th><th>Kader</th><th>Object</th><th>Relatie</th><th>Rationale</th><th>Implementatiebewijs</th></tr></thead>
      <tbody id="crosswalk-rows"><tr><td colspan="6">Mappings laden…</td></tr></tbody>
    </table>
  </div>
  <p id="crosswalk-boundary" class="muted"></p>
</article>
'''

_CSS = r'''
<style id="governance-crosswalk-style">
.governance-crosswalk #crosswalk-table{min-width:1120px}.crosswalk-control strong{display:block}.crosswalk-object code{font-weight:800}.crosswalk-relation{font-weight:800}.crosswalk-relation[data-relation="supports"]{color:#16803c}.crosswalk-relation[data-relation="partial-support"]{color:#9a3412}.crosswalk-relation[data-relation="context-only"],.crosswalk-relation[data-relation$="context"]{color:#475467}.crosswalk-refs{max-width:300px;overflow-wrap:anywhere}.crosswalk-source{font-size:.78rem;overflow-wrap:anywhere}
</style>
'''

_SCRIPT_TAG = '<script src="/ui/governance-crosswalk-experience.js" defer></script>'


def extend_console_page(page: str) -> str:
    if 'id="governance-crosswalk"' in page:
        return page
    marker = '<article class="surface" id="governance-knowledge"'
    if marker not in page:
        raise RuntimeError("canonical Governance knowledge marker not found")
    extended = page.replace(marker, _PANEL + marker, 1)
    extended = extended.replace("</head>", _CSS + "</head>", 1)
    extended = extended.replace("</body>", _SCRIPT_TAG + "</body>", 1)
    return extended


_PAGE = extend_console_page(FRAMEWORK_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def governance_crosswalk_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const panel = document.getElementById('governance-crosswalk');
  if (!panel) return;

  function flatten(payload) {
    const rows = [];
    for (const control of payload.controls || []) {
      for (const mapping of control.mappings || []) rows.push({control, mapping});
    }
    return rows;
  }

  function renderSummary(payload, rows) {
    const counts = payload.mapping_count_by_framework || {};
    $('crosswalk-summary').innerHTML = `
      <article><span>DTMO-controls</span><strong>${esc((payload.controls || []).length)}</strong><small>concrete capabilities</small></article>
      <article><span>Expliciete relaties</span><strong>${esc(payload.mapping_count || rows.length)}</strong><small>geen inferred mappings</small></article>
      <article><span>Normenkader IBP</span><strong>${esc(counts['normenkader-ibp'] || 0)}</strong><small>controlrelaties</small></article>
      <article><span>MITRE ATT&CK</span><strong>${esc(counts['mitre-attack'] || 0)}</strong><small>threat-context</small></article>
      <article><span>NIST CSF</span><strong>${esc(counts['nist-csf'] || 0)}</strong><small>outcome-relaties</small></article>
      <article><span>CVSS</span><strong>${esc(counts.cvss || 0)}</strong><small>context only</small></article>`;
  }

  function renderRows(rows) {
    $('crosswalk-rows').innerHTML = rows.map(({control, mapping}) => `
      <tr>
        <td class="crosswalk-control"><strong>${esc(control.dtmo_control_id)}</strong>${esc(control.title)}</td>
        <td>${esc(mapping.framework_id)}</td>
        <td class="crosswalk-object"><code>${esc(mapping.object_id)}</code><br>${esc(mapping.object_title)}</td>
        <td><span class="crosswalk-relation" data-relation="${esc(mapping.relationship)}">${esc(mapping.relationship)}</span></td>
        <td>${esc(mapping.rationale)}<br><span class="crosswalk-source">Bron: ${esc(mapping.source_url)}</span></td>
        <td class="crosswalk-refs">${(control.implementation_refs || []).map(ref => `<code>${esc(ref)}</code>`).join('<br>')}</td>
      </tr>`).join('');
  }

  async function loadCrosswalk() {
    $('crosswalk-status').textContent = 'Expliciete mappings laden…';
    try {
      const payload = await api('/api/v1/governance/control-crosswalk');
      const rows = flatten(payload);
      renderSummary(payload, rows);
      renderRows(rows);
      $('crosswalk-boundary').textContent = payload.claim_boundary || '';
      $('crosswalk-status').textContent = `${rows.length} expliciete relaties geladen · geverifieerd ${payload.verified_on || 'onbekend'}.`;
    } catch (error) {
      $('crosswalk-status').textContent = `Crosswalk niet beschikbaar: ${error.message}`;
      $('crosswalk-rows').innerHTML = `<tr><td colspan="6">${esc(error.message)}</td></tr>`;
    }
  }

  $('crosswalk-refresh')?.addEventListener('click', () => void loadCrosswalk());
  void loadCrosswalk();
})();
'''


@router.get("/ui/governance-crosswalk-experience.js", include_in_schema=False)
def governance_crosswalk_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})
