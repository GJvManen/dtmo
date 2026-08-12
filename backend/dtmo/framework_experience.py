from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

from dtmo.analytics_experience import _PAGE as ANALYTICS_CONSOLE_PAGE

router = APIRouter()

_PANEL = r'''
<article class="surface framework-governance" id="framework-governance" style="margin-top:1rem">
  <div class="page-heading">
    <div>
      <p class="eyebrow">First-class framework governance</p>
      <h3>Kaders & expliciete mappings</h3>
      <p>Versioneerde kaders met dekking, reviewstatus en provenance. DTMO toont ontbrekende mappings als UNMAPPED en leidt geen equivalenties af uit tags of vrije tekst.</p>
    </div>
    <button id="framework-refresh" class="button secondary" type="button">Kaders vernieuwen</button>
  </div>
  <div id="framework-status" class="status" role="status" aria-live="polite">Frameworkinventaris laden…</div>
  <div id="framework-summary" class="framework-summary" aria-label="Frameworkstatistieken"></div>
  <div id="framework-cards" class="framework-grid" data-testid="framework-cards"></div>
  <section class="framework-detail" aria-labelledby="framework-detail-title">
    <div class="page-heading"><div><h4 id="framework-detail-title">Mappingdetails</h4><p class="muted">Selecteer een kader om de expliciete mappings, intelligence en reviewstatus te bekijken.</p></div></div>
    <div id="framework-detail-body" class="empty-state">Nog geen kader geselecteerd.</div>
  </section>
</article>
'''

_CSS = r'''
<style id="e5-e7-framework-style">
.framework-summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.65rem;margin:.75rem 0 1rem}.framework-summary article{border:1px solid var(--line);border-radius:10px;padding:.75rem;background:var(--surface-2)}.framework-summary strong{display:block;font-size:1.45rem}.framework-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:.8rem}.framework-card{border:1px solid var(--line);border-radius:12px;padding:1rem;background:var(--surface-2)}.framework-card h4{margin:.2rem 0}.framework-meta{display:flex;gap:.4rem;flex-wrap:wrap;margin:.45rem 0}.framework-kpis{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.4rem;margin:.7rem 0}.framework-kpis span{padding:.4rem;border:1px solid var(--line);border-radius:8px;font-size:.82rem}.framework-state{font-weight:800;letter-spacing:.02em}.framework-state.mapped{color:#16803c}.framework-state.unmapped{color:#667085}.framework-state.context-only{color:#9a3412}.framework-detail{margin-top:1rem}.framework-table-wrap{overflow-x:auto}.framework-table-wrap table{min-width:920px}.mapping-review.pending{color:#9a3412;font-weight:800}.mapping-review.approved{color:#16803c;font-weight:800}.mapping-review.rejected{color:#b42318;font-weight:800}.framework-provenance{max-width:320px;overflow-wrap:anywhere}.coverage-meter{height:.55rem;border-radius:999px;background:var(--line);overflow:hidden;margin:.5rem 0}.coverage-meter span{display:block;height:100%;background:currentColor}.framework-card[data-status="MAPPED"]{color:inherit;border-left:5px solid #16803c}.framework-card[data-status="UNMAPPED"]{color:inherit;border-left:5px solid #667085}.framework-card[data-status="CONTEXT_ONLY"]{color:inherit;border-left:5px solid #c2410c}
</style>
'''

_SCRIPT_TAG = '<script src="/ui/framework-experience.js" defer></script>'


def extend_console_page(page: str) -> str:
    if 'id="framework-governance"' in page:
        return page
    marker = '<article class="surface" id="governance-knowledge"'
    if marker not in page:
        raise RuntimeError("canonical Governance knowledge marker not found")
    extended = page.replace(marker, _PANEL + marker, 1)
    extended = extended.replace("</head>", _CSS + "</head>", 1)
    extended = extended.replace("</body>", _SCRIPT_TAG + "</body>", 1)
    return extended


_PAGE = extend_console_page(ANALYTICS_CONSOLE_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def framework_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const panel = document.getElementById('framework-governance');
  if (!panel) return;

  function stateClass(status) {
    return String(status || '').toLowerCase().replace('_','-');
  }

  function coverageLabel(framework) {
    if (framework.status === 'CONTEXT_ONLY') return 'Context only';
    if (framework.coverage_percent === null || framework.coverage_percent === undefined) {
      return `${framework.mapped_object_count || 0} expliciet gemapte objecten`;
    }
    return `${Number(framework.coverage_percent).toFixed(1)}% van ${framework.expected_object_count} bekende objecten`;
  }

  function renderSummary(frameworks) {
    const counts = frameworks.reduce((acc, framework) => {
      acc[framework.status] = (acc[framework.status] || 0) + 1;
      acc.pending += Number(framework.pending_mapping_count || 0);
      acc.approved += Number(framework.approved_mapping_count || 0);
      return acc;
    }, {MAPPED:0,UNMAPPED:0,CONTEXT_ONLY:0,pending:0,approved:0});
    $('framework-summary').innerHTML = `
      <article><span>Kaders</span><strong>${esc(frameworks.length)}</strong><small>versioned inventory</small></article>
      <article><span>Gemapt</span><strong>${esc(counts.MAPPED)}</strong><small>minimaal één goedgekeurde mapping</small></article>
      <article><span>UNMAPPED</span><strong>${esc(counts.UNMAPPED)}</strong><small>geen goedgekeurde mapping</small></article>
      <article><span>Pending review</span><strong>${esc(counts.pending)}</strong><small>telt nog niet als dekking</small></article>
      <article><span>Approved mappings</span><strong>${esc(counts.approved)}</strong><small>expliciet beoordeeld</small></article>`;
  }

  function renderCards(frameworks) {
    $('framework-cards').innerHTML = frameworks.map((framework) => {
      const statusClass = stateClass(framework.status);
      const meter = framework.coverage_percent === null || framework.coverage_percent === undefined ? '' : `<div class="coverage-meter" title="${esc(coverageLabel(framework))}"><span style="width:${Math.min(100,Math.max(0,Number(framework.coverage_percent)))}%"></span></div>`;
      const scope = framework.metadata?.information_security_norms !== undefined ? `<p class="muted">${esc(framework.metadata.information_security_norms)} IB-normen · ${esc(framework.metadata.privacy_norms)} privacynormen</p>` : '';
      return `<article class="framework-card" data-status="${esc(framework.status)}" data-framework-id="${esc(framework.id)}">
        <div class="page-heading"><div><p class="eyebrow">${esc(framework.authority)}</p><h4>${esc(framework.name)}</h4></div><span class="framework-state ${statusClass}">${esc(framework.status)}</span></div>
        <div class="framework-meta"><span class="status-pill neutral">${esc(framework.version_label)}</span><span class="status-pill neutral">${esc(framework.kind)}</span></div>
        ${scope}${meter}<p>${esc(coverageLabel(framework))}</p>
        <div class="framework-kpis"><span>Approved: <strong>${esc(framework.approved_mapping_count || 0)}</strong></span><span>Pending: <strong>${esc(framework.pending_mapping_count || 0)}</strong></span><span>Rejected: <strong>${esc(framework.rejected_mapping_count || 0)}</strong></span><span>Objects: <strong>${esc(framework.mapped_object_count || 0)}</strong></span></div>
        <p class="muted-code">Verified: ${esc(new Date(framework.last_verified_at).toLocaleDateString())}</p>
        <button class="button secondary" type="button" data-framework-detail="${esc(framework.id)}">Bekijk mappings</button>
      </article>`;
    }).join('');
  }

  function renderDetail(payload) {
    const framework = payload.framework || {};
    const mappings = payload.mappings || [];
    $('framework-detail-title').textContent = `${framework.name || 'Kader'} — ${framework.version_label || framework.version || ''}`;
    if (!mappings.length) {
      $('framework-detail-body').innerHTML = `<div class="empty-state"><strong>${esc(framework.status || 'UNMAPPED')}</strong><p>Geen expliciete mappings beschikbaar. DTMO leidt geen control- of technique-equivalentie af uit tags, titels of vrije tekst.</p></div>`;
      return;
    }
    const rows = mappings.map((mapping) => `<tr>
      <td>${esc(mapping.object_type)}<br><strong>${esc(mapping.object_id)}</strong>${mapping.object_title?`<br>${esc(mapping.object_title)}`:''}</td>
      <td>${esc(mapping.intelligence_title || mapping.intelligence_id)}</td>
      <td>${esc(mapping.mapping_status)}</td>
      <td>${esc(mapping.confidence_score)}%</td>
      <td><span class="mapping-review ${esc(mapping.review_state)}">${esc(mapping.review_state)}</span><br><small>${esc(mapping.reviewed_by || 'nog niet beoordeeld')}</small></td>
      <td class="framework-provenance">${esc(mapping.provenance_reference)}<br><small>${esc(mapping.mapping_reason)}</small></td>
    </tr>`).join('');
    $('framework-detail-body').innerHTML = `<div class="framework-table-wrap"><table><thead><tr><th>Control/techniek</th><th>Intelligence</th><th>Type</th><th>Confidence</th><th>Review</th><th>Provenance & reden</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  }

  async function loadFrameworks() {
    $('framework-status').textContent = 'Frameworkinventaris laden…';
    try {
      const payload = await api('/api/v1/governance/frameworks');
      const frameworks = payload.frameworks || [];
      renderSummary(frameworks);
      renderCards(frameworks);
      $('framework-status').textContent = `${frameworks.length} versioneerde kaders geladen · policy: expliciete provenance + menselijke review.`;
    } catch (error) {
      $('framework-status').textContent = `Frameworkinventaris niet beschikbaar: ${error.message}`;
    }
  }

  $('framework-cards')?.addEventListener('click', async (event) => {
    const button = event.target.closest('[data-framework-detail]');
    if (!button) return;
    $('framework-detail-body').textContent = 'Mappingdetails laden…';
    try {
      const payload = await api(`/api/v1/governance/frameworks/${encodeURIComponent(button.dataset.frameworkDetail)}`);
      renderDetail(payload);
    } catch (error) {
      $('framework-detail-body').textContent = `Mappingdetails niet beschikbaar: ${error.message}`;
    }
  });
  $('framework-refresh')?.addEventListener('click', () => void loadFrameworks());
  void loadFrameworks();
})();
'''


@router.get("/ui/framework-experience.js", include_in_schema=False)
def framework_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})
