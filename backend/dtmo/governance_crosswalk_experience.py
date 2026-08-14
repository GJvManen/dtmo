from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

from dtmo.framework_experience import _PAGE as FRAMEWORK_PAGE
from dtmo.framework_experience import _SCRIPT as FRAMEWORK_SCRIPT

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

_DYNAMIC_CSS = r'''
.governance-crosswalk #crosswalk-table{min-width:1120px}.crosswalk-control strong{display:block}.crosswalk-object code{font-weight:800}.crosswalk-relation{font-weight:800}.crosswalk-relation[data-relation="supports"]{color:#7ee2a8}.crosswalk-relation[data-relation="partial-support"]{color:#fdba74}.crosswalk-relation[data-relation="context-only"],.crosswalk-relation[data-relation$="context"]{color:#d7e3f1}.crosswalk-refs{max-width:300px;overflow-wrap:anywhere}.crosswalk-source{font-size:.78rem;overflow-wrap:anywhere}
/* Owner-acceptance contrast repair: severity classes must never recolor an entire recent-intelligence card. */
.card.severity-card{color:var(--text)!important}.card.severity-card .intel-meta>span:not(.severity-pill){color:#d7e3f1!important}.card.severity-card p{color:var(--text)!important}.card.severity-card a{color:#9bd3ff!important;text-decoration:underline;text-underline-offset:.15em}.card.severity-card .severity-pill{background:var(--surface)!important}.card.severity-card.severity-informational .severity-pill{color:#d7e3f1!important}.card.severity-card.severity-low .severity-pill{color:#86efac!important}.card.severity-card.severity-medium .severity-pill{color:#fdba74!important}.card.severity-card.severity-high .severity-pill{color:#fca5a5!important}.card.severity-card.severity-critical .severity-pill{color:#fecaca!important}
'''

_CSS = f'<style id="governance-crosswalk-style">{_DYNAMIC_CSS}</style>'
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


_SCRIPT = rf'''
(() => {{
  const panelMarkup = {repr(_PANEL)};
  const cssText = {repr(_DYNAMIC_CSS)};

  function ensureStyle() {{
    if (document.getElementById('governance-crosswalk-style')) return;
    const style = document.createElement('style');
    style.id = 'governance-crosswalk-style';
    style.textContent = cssText;
    document.head.appendChild(style);
  }}

  function ensurePanel() {{
    let panel = document.getElementById('governance-crosswalk');
    if (panel) return panel;
    const framework = document.getElementById('framework-governance');
    const knowledge = document.getElementById('governance-knowledge');
    if (framework) {{
      framework.insertAdjacentHTML('afterend', panelMarkup);
    }} else if (knowledge) {{
      knowledge.insertAdjacentHTML('beforebegin', panelMarkup);
    }} else {{
      const host = document.querySelector('[data-view-panel="governance"]');
      if (!host) return null;
      host.insertAdjacentHTML('beforeend', panelMarkup);
    }}
    return document.getElementById('governance-crosswalk');
  }}

  ensureStyle();
  const panel = ensurePanel();
  if (!panel || panel.dataset.crosswalkInitialized === 'true') return;
  panel.dataset.crosswalkInitialized = 'true';

  function flatten(payload) {{
    const rows = [];
    for (const control of payload.controls || []) {{
      for (const mapping of control.mappings || []) rows.push({{control, mapping}});
    }}
    return rows;
  }}

  function renderSummary(payload, rows) {{
    const counts = payload.mapping_count_by_framework || {{}};
    $('crosswalk-summary').innerHTML = `
      <article><span>DTMO-controls</span><strong>${{esc((payload.controls || []).length)}}</strong><small>concrete capabilities</small></article>
      <article><span>Expliciete relaties</span><strong>${{esc(payload.mapping_count || rows.length)}}</strong><small>geen inferred mappings</small></article>
      <article><span>Normenkader IBP</span><strong>${{esc(counts['normenkader-ibp'] || 0)}}</strong><small>controlrelaties</small></article>
      <article><span>MITRE ATT&CK</span><strong>${{esc(counts['mitre-attack'] || 0)}}</strong><small>threat-context</small></article>
      <article><span>NIST CSF</span><strong>${{esc(counts['nist-csf'] || 0)}}</strong><small>outcome-relaties</small></article>
      <article><span>CVSS</span><strong>${{esc(counts.cvss || 0)}}</strong><small>context only</small></article>`;
  }}

  function renderRows(rows) {{
    $('crosswalk-rows').innerHTML = rows.map(({{control, mapping}}) => `
      <tr>
        <td class="crosswalk-control"><strong>${{esc(control.dtmo_control_id)}}</strong>${{esc(control.title)}}</td>
        <td>${{esc(mapping.framework_id)}}</td>
        <td class="crosswalk-object"><code>${{esc(mapping.object_id)}}</code><br>${{esc(mapping.object_title)}}</td>
        <td><span class="crosswalk-relation" data-relation="${{esc(mapping.relationship)}}">${{esc(mapping.relationship)}}</span></td>
        <td>${{esc(mapping.rationale)}}<br><span class="crosswalk-source">Bron: ${{esc(mapping.source_url)}}</span></td>
        <td class="crosswalk-refs">${{(control.implementation_refs || []).map(ref => `<code>${{esc(ref)}}</code>`).join('<br>')}}</td>
      </tr>`).join('');
  }}

  async function loadCrosswalk() {{
    $('crosswalk-status').textContent = 'Expliciete mappings laden…';
    try {{
      const payload = await api('/api/v1/governance/control-crosswalk');
      const rows = flatten(payload);
      renderSummary(payload, rows);
      renderRows(rows);
      $('crosswalk-boundary').textContent = payload.claim_boundary || '';
      $('crosswalk-status').textContent = `${{rows.length}} expliciete relaties geladen · geverifieerd ${{payload.verified_on || 'onbekend'}}.`;
    }} catch (error) {{
      $('crosswalk-status').textContent = `Crosswalk niet beschikbaar: ${{error.message}}`;
      $('crosswalk-rows').innerHTML = `<tr><td colspan="6">${{esc(error.message)}}</td></tr>`;
    }}
  }}

  $('crosswalk-refresh')?.addEventListener('click', () => void loadCrosswalk());
  void loadCrosswalk();
}})();
'''


@router.get("/ui/governance-crosswalk-experience.js", include_in_schema=False)
def governance_crosswalk_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})


# The highest-level canonical console is currently composed by the E3/E6 layers from
# FRAMEWORK_PAGE. Those layers therefore request the framework script without carrying
# the later server-side crosswalk composition. This route intentionally wins before the
# framework router in main.py and augments that existing script with the owner-acceptance
# crosswalk/contrast repair, keeping the canonical root coherent without duplicating UI.
@router.get("/ui/framework-experience.js", include_in_schema=False)
def framework_script_with_crosswalk() -> Response:
    return Response(
        FRAMEWORK_SCRIPT + "\n" + _SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )
