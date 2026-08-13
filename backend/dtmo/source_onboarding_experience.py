from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

from dtmo.framework_experience import _PAGE as FRAMEWORK_CONSOLE_PAGE

router = APIRouter()

_PANEL = r'''
<article class="surface source-onboarding" id="source-onboarding" style="margin-bottom:1rem">
  <div class="page-heading">
    <div>
      <p class="eyebrow">Governed manual onboarding</p>
      <h3>Nieuwe intelligencebron registreren</h3>
      <p>Nieuwe handmatige bronnen worden altijd uitgeschakeld aangemaakt. Valideer configuratie en voer een niet-ingestende pre-activation test uit voordat een bevoegde operator de bron afzonderlijk activeert.</p>
    </div>
    <span class="status-pill neutral">Disabled-first</span>
  </div>
  <form id="source-onboarding-form" class="source-onboarding-form">
    <label>Source ID<input id="onboarding-source-id" required pattern="[a-z0-9_-]+" placeholder="sector-feed"></label>
    <label>Naam<input id="onboarding-source-name" required minlength="2" placeholder="Sector advisory feed"></label>
    <label>Source type<select id="onboarding-source-type"><option value="json-feed">DTMO JSON v1 feed</option></select></label>
    <label>Betrouwbaarheid<select id="onboarding-reliability"><option>authoritative</option><option>high</option><option selected>medium</option><option>low</option></select></label>
    <label class="span-2">HTTPS endpoint<input id="onboarding-endpoint" type="url" required placeholder="https://example.org/feed.json"></label>
    <label>Schedule / freshness (sec)<input id="onboarding-interval" type="number" min="60" max="86400" value="3600"></label>
    <label>Authentication mode<select id="onboarding-auth-mode"><option value="anonymous">Anonymous</option><option value="secret-reference">Logical secret reference</option></select></label>
    <label class="span-2" id="onboarding-secret-row" hidden>Logical secret reference<input id="onboarding-secret-ref" placeholder="env:SOURCE_TOKEN" autocomplete="off"><small>Alleen een logische verwijzing; ruwe credentials worden geweigerd.</small></label>
    <label class="span-2">Owner<input id="onboarding-owner" readonly value="Current authenticated human administrator"><small>De server legt de geauthenticeerde menselijke actor vast als eigenaar/creator.</small></label>
    <div class="span-2 source-onboarding-boundary"><strong>Activation state: Disabled</strong><span>Activeren is een afzonderlijke, geauditeerde handeling na validatie/test.</span></div>
    <div class="span-2 actions"><button class="button" type="submit">Bron disabled registreren</button><button class="button secondary" id="onboarding-refresh" type="button">Onboardinglijst vernieuwen</button></div>
  </form>
  <div id="source-onboarding-status" class="status" role="status" aria-live="polite">Nog geen onboardingactie uitgevoerd.</div>
  <div id="source-onboarding-list" class="cards" data-testid="source-onboarding-list"></div>
</article>
'''

_CSS = r'''
<style id="e3-source-onboarding-style">
.source-onboarding-form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem}.source-onboarding-form label{display:grid;gap:.35rem}.source-onboarding-form .span-2{grid-column:1/-1}.source-onboarding-form small{color:var(--muted)}.source-onboarding-boundary{display:flex;gap:.75rem;align-items:center;flex-wrap:wrap;padding:.7rem;border:1px solid var(--line);border-radius:10px;background:var(--surface-2)}.onboarding-card{border:1px solid var(--line);border-radius:12px;padding:1rem;background:var(--surface-2)}.onboarding-card header{display:flex;justify-content:space-between;gap:1rem;align-items:flex-start}.onboarding-meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.35rem .75rem;margin:.65rem 0}.onboarding-meta span{font-size:.86rem;color:var(--muted)}.onboarding-actions{display:flex;gap:.5rem;flex-wrap:wrap}.onboarding-check{font-size:.85rem;margin-top:.55rem}.onboarding-check.good{color:#16803c}.onboarding-check.bad{color:#b42318}@media(max-width:760px){.source-onboarding-form{grid-template-columns:1fr}.source-onboarding-form .span-2{grid-column:1}}
</style>
'''

_SCRIPT_TAG = '<script src="/ui/source-onboarding-experience.js" defer></script>'


def extend_console_page(page: str) -> str:
    if 'id="source-onboarding"' in page:
        return page
    marker = '<div id="source-status" class="status" role="status" data-testid="source-status"></div>'
    if marker not in page:
        raise RuntimeError("canonical Sources & Catalog marker not found")
    extended = page.replace(marker, _PANEL + marker, 1)
    extended = extended.replace("</head>", _CSS + "</head>", 1)
    extended = extended.replace("</body>", _SCRIPT_TAG + "</body>", 1)
    return extended


_PAGE = extend_console_page(FRAMEWORK_CONSOLE_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def source_onboarding_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const form = document.getElementById('source-onboarding-form');
  if (!form) return;
  const state = new Map();
  const status = (text) => { const node=$('source-onboarding-status'); if(node) node.textContent=text; };

  function authMode(source) {
    return source.authentication_mode || (source.secret_ref ? 'credentialed-secret-reference' : 'anonymous');
  }

  function render(sources) {
    const list = $('source-onboarding-list');
    if (!list) return;
    list.innerHTML = sources.length ? sources.map((source) => {
      const checks = state.get(source.id) || {};
      const validation = checks.validated === true ? '<div class="onboarding-check good">✓ Configuratie gevalideerd</div>' : (checks.validated === false ? '<div class="onboarding-check bad">✕ Validatie mislukt</div>' : '<div class="onboarding-check">Nog niet gevalideerd in deze sessie</div>');
      const tested = checks.tested === true ? '<div class="onboarding-check good">✓ Pre-activation test geslaagd · geen ingest</div>' : (checks.tested === false ? '<div class="onboarding-check bad">✕ Pre-activation test mislukt</div>' : '<div class="onboarding-check">Nog geen pre-activation test in deze sessie</div>');
      const canActivate = !source.enabled && checks.validated === true && checks.tested === true;
      return `<article class="onboarding-card" data-onboarding-id="${esc(source.id)}"><header><div><strong>${esc(source.name)}</strong><div class="muted-code">${esc(source.id)}</div></div><span class="status-pill ${source.enabled?'good':'neutral'}">${source.enabled?'Actief':'Disabled'}</span></header><div class="onboarding-meta"><span>Owner: ${esc(source.owner || source.created_by)}</span><span>Auth: ${esc(authMode(source))}</span><span>Schedule/freshness: ${esc(source.interval_seconds)}s</span><span>Type: ${esc(source.source_type)}</span><span>Reliability: ${esc(source.reliability)}</span><span>Secret: ${source.secret_ref?'logical reference configured':'geen'}</span><span style="grid-column:1/-1">${esc(source.endpoint_url)}</span></div>${validation}${tested}<div class="onboarding-actions"><button class="button secondary" type="button" data-onboarding-validate="${esc(source.id)}">Valideer configuratie</button><button class="button secondary" type="button" data-onboarding-test="${esc(source.id)}" ${source.enabled?'disabled':''}>Pre-activation test</button><button class="button" type="button" data-onboarding-enable="${esc(source.id)}" ${canActivate?'':'disabled'}>Afzonderlijk activeren</button></div></article>`;
    }).join('') : '<div class="empty-state"><strong>Nog geen handmatige of gebootstrapte bronnen.</strong></div>';
  }

  async function refresh() {
    try {
      const sources = await api('/api/v1/admin/sources');
      render(sources);
      status(`${sources.length} geregistreerde bronnen · nieuwe bronnen starten disabled.`);
    } catch (error) {
      status(`Onboardinglijst niet beschikbaar: ${error.message}`);
    }
  }

  $('onboarding-auth-mode')?.addEventListener('change', (event) => {
    const secretMode = event.target.value === 'secret-reference';
    $('onboarding-secret-row').hidden = !secretMode;
    if (!secretMode) $('onboarding-secret-ref').value = '';
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const secretMode = $('onboarding-auth-mode').value === 'secret-reference';
    const secretRef = secretMode ? $('onboarding-secret-ref').value.trim() : '';
    if (secretMode && !secretRef) {
      status('Logical secret reference is verplicht voor deze authentication mode.');
      return;
    }
    const payload = {
      id: $('onboarding-source-id').value.trim(),
      name: $('onboarding-source-name').value.trim(),
      source_type: $('onboarding-source-type').value,
      endpoint_url: $('onboarding-endpoint').value.trim(),
      enabled: false,
      interval_seconds: Number($('onboarding-interval').value),
      reliability: $('onboarding-reliability').value,
      secret_ref: secretRef || null,
    };
    try {
      const created = await api('/api/v1/admin/sources', {method:'POST', body:JSON.stringify(payload)});
      state.set(created.id, {validated:false,tested:false});
      form.reset();
      $('onboarding-interval').value='3600';
      $('onboarding-secret-row').hidden=true;
      status(`${created.name} geregistreerd als Disabled. Valideer en test vóór activatie.`);
      await refresh();
    } catch (error) {
      status(`Registratie mislukt: ${error.message}`);
    }
  });

  $('source-onboarding-list')?.addEventListener('click', async (event) => {
    const validateButton = event.target.closest('[data-onboarding-validate]');
    const testButton = event.target.closest('[data-onboarding-test]');
    const enableButton = event.target.closest('[data-onboarding-enable]');
    const id = validateButton?.dataset.onboardingValidate || testButton?.dataset.onboardingTest || enableButton?.dataset.onboardingEnable;
    if (!id) return;
    const checks = state.get(id) || {};
    try {
      if (validateButton) {
        const result = await api(`/api/v1/admin/sources/${encodeURIComponent(id)}/validate`, {method:'POST'});
        checks.validated = result.valid === true;
        if (!checks.validated) checks.tested = false;
        state.set(id, checks);
        status(result.valid ? `${id}: configuratie geldig.` : `${id}: ${result.reason || 'validatie mislukt'}`);
      } else if (testButton) {
        if (checks.validated !== true) { status(`${id}: valideer eerst de configuratie.`); return; }
        const result = await api(`/api/v1/admin/sources/${encodeURIComponent(id)}/test`, {method:'POST'});
        checks.tested = result.status === 'completed' && result.ingested === false;
        state.set(id, checks);
        status(checks.tested ? `${id}: pre-activation test geslaagd (${result.records} records gezien, niets ingested).` : `${id}: test mislukt: ${result.error || result.status}`);
      } else if (enableButton) {
        if (checks.validated !== true || checks.tested !== true) { status(`${id}: validatie én pre-activation test zijn vereist vóór activatie.`); return; }
        await api(`/api/v1/admin/sources/${encodeURIComponent(id)}`, {method:'PATCH', body:JSON.stringify({enabled:true})});
        status(`${id}: afzonderlijk geactiveerd. Normale source run blijft onder bestaande RBAC/audit/publication boundaries.`);
      }
      await refresh();
    } catch (error) {
      if (testButton) checks.tested = false;
      state.set(id, checks);
      status(`${id}: onboardingactie mislukt: ${error.message}`);
      await refresh();
    }
  });

  $('onboarding-refresh')?.addEventListener('click', () => void refresh());
  void refresh();
})();
'''


@router.get("/ui/source-onboarding-experience.js", include_in_schema=False)
def source_onboarding_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})
