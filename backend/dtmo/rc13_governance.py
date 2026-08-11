from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

from dtmo.rc13_administration import _PAGE as ADMIN_CONSOLE_PAGE

router = APIRouter()

_GOVERNANCE_START = '<section class="view" data-view-panel="governance">'
_GOVERNANCE_END = "</section>\n</main>"

_GOVERNANCE_PANEL = r'''
<article class="surface" id="governance-knowledge" style="margin-top:1rem">
  <div class="page-heading">
    <div>
      <p class="eyebrow">Repository-backed knowledge</p>
      <h3>Frameworks, mappings & authority boundaries</h3>
      <p>Toont alleen mappings met expliciete repository-provenance. Ontbrekende externe crosswalks worden zichtbaar als niet gemapt en nooit afgeleid.</p>
    </div>
    <button id="governance-refresh" class="button secondary" type="button">Vernieuwen</button>
  </div>
  <div id="governance-status" class="status" role="status" aria-live="polite">Governance knowledge laden…</div>
  <section aria-labelledby="governance-frameworks-title">
    <h4 id="governance-frameworks-title">Frameworkdekking</h4>
    <div id="governance-frameworks" class="cards"></div>
  </section>
  <section aria-labelledby="governance-mappings-title" style="margin-top:1rem">
    <h4 id="governance-mappings-title">Daadwerkelijke DTMO-governance mappings</h4>
    <p class="muted">Deze mappings verwijzen naar concrete repository-evidence; ze zijn geen externe framework-equivalenties.</p>
    <div id="governance-mappings" class="cards"></div>
  </section>
  <section aria-labelledby="governance-boundaries-title" style="margin-top:1rem">
    <h4 id="governance-boundaries-title">Niet-onderhandelbare beslisgrenzen</h4>
    <div id="governance-boundaries" class="cards"></div>
  </section>
  <div id="governance-claim-boundary" class="diagnostic" role="note"></div>
</article>
'''

_SCRIPT_TAG = '<script src="/ui/rc13-governance.js" defer></script>'


def extend_console_page(page: str) -> str:
    governance_start = page.find(_GOVERNANCE_START)
    if governance_start < 0:
        raise RuntimeError("canonical Governance section marker not found")
    governance_end = page.find(_GOVERNANCE_END, governance_start)
    if governance_end < 0:
        raise RuntimeError("canonical Governance section boundary not found")
    extended = page[:governance_end] + _GOVERNANCE_PANEL + page[governance_end:]
    if _SCRIPT_TAG not in extended:
        extended = extended.replace("</body>", _SCRIPT_TAG + "</body>")
    return extended


_PAGE = extend_console_page(ADMIN_CONSOLE_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def rc13_governance_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const panel = document.getElementById('governance-knowledge');
  if (!panel) return;

  const storage = {
    subject: () => sessionStorage.getItem('dtmo.subject') || 'admin-tester',
    roles: () => sessionStorage.getItem('dtmo.roles') || 'admin',
    apiKey: () => sessionStorage.getItem('dtmo.apiKey') || '',
  };
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

  async function governanceApi() {
    const response = await fetch('/api/v1/governance/knowledge', {
      headers: {
        'X-DTMO-Subject': storage.subject(),
        'X-DTMO-Roles': storage.roles(),
        'X-DTMO-API-Key': storage.apiKey(),
      },
    });
    let body = {};
    try { body = await response.json(); } catch (_) { body = {}; }
    if (!response.ok) throw new Error(body.detail || `HTTP ${response.status}`);
    return body;
  }

  function frameworkClass(coverage) {
    return coverage === 'mapped_internal' ? 'good' : 'neutral';
  }

  function renderFrameworks(frameworks) {
    const target = document.getElementById('governance-frameworks');
    target.innerHTML = frameworks.map((framework) => `<article class="card" data-governance-framework="${esc(framework.id)}">
      <div class="page-heading"><div><strong>${esc(framework.name)}</strong><p>${esc(framework.kind)}</p></div><span class="status-pill ${frameworkClass(framework.coverage)}">${esc(framework.coverage_label)}</span></div>
      <p>${esc(framework.note)}</p>
      <p class="muted-code">Provenance: ${(framework.provenance || []).map(esc).join(' · ') || 'geen'}</p>
      <p class="muted-code">Mapping IDs: ${(framework.mapping_ids || []).map(esc).join(' · ') || 'geen — geen equivalence geclaimd'}</p>
    </article>`).join('');
  }

  function renderMappings(mappings) {
    const target = document.getElementById('governance-mappings');
    target.innerHTML = mappings.map((mapping) => `<article class="card" data-governance-mapping="${esc(mapping.id)}">
      <strong>${esc(mapping.title)}</strong>
      <p>${esc(mapping.statement)}</p>
      <p class="muted-code">${esc(mapping.source)} → ${esc(mapping.section)}</p>
    </article>`).join('');
  }

  function renderBoundaries(boundaries) {
    const target = document.getElementById('governance-boundaries');
    target.innerHTML = boundaries.map((boundary, index) => `<article class="card" data-governance-boundary="${index + 1}"><strong>Boundary ${index + 1}</strong><p>${esc(boundary)}</p></article>`).join('');
  }

  async function loadGovernance() {
    const status = document.getElementById('governance-status');
    status.textContent = 'Governance knowledge laden…';
    try {
      const snapshot = await governanceApi();
      renderFrameworks(snapshot.frameworks || []);
      renderMappings(snapshot.mappings || []);
      renderBoundaries(snapshot.authority_boundaries || []);
      document.getElementById('governance-claim-boundary').textContent = snapshot.claim_boundary || '';
      status.textContent = `${(snapshot.frameworks || []).length} frameworks · ${(snapshot.mappings || []).length} repository-backed mappings.`;
    } catch (error) {
      status.textContent = `Governance knowledge niet beschikbaar: ${error.message}`;
    }
  }

  document.getElementById('governance-refresh').addEventListener('click', () => void loadGovernance());
  void loadGovernance();
})();
'''


@router.get("/ui/rc13-governance.js", include_in_schema=False)
def rc13_governance_script() -> Response:
    return Response(
        _SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )
