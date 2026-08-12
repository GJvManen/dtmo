from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.intelligence.model import IntelligenceSeverity
from dtmo.persistence.models import IntelligenceItem
from dtmo.rc13_governance import _PAGE as GOVERNANCE_CONSOLE_PAGE

router = APIRouter()

_SEVERITY_ORDER = tuple(item.value for item in IntelligenceSeverity)
LimitParam = Annotated[int, Query(ge=1, le=100)]
SeverityFilter = Annotated[list[str] | None, Query()]


def _selected_severities(values: list[str] | None) -> tuple[IntelligenceSeverity, ...]:
    if not values:
        return tuple(IntelligenceSeverity)
    selected: list[IntelligenceSeverity] = []
    for value in values:
        try:
            severity = IntelligenceSeverity(value.strip().lower())
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"unsupported severity filter: {value}",
            ) from exc
        if severity not in selected:
            selected.append(severity)
    return tuple(selected)


def _enum_value(value: object) -> str:
    return str(getattr(value, "value", value))


def _serialize(item: IntelligenceItem) -> dict[str, object]:
    return {
        "id": str(item.id),
        "source_id": item.source_id,
        "title": item.title,
        "summary": item.summary,
        "severity": _enum_value(item.severity),
        "confidence_score": item.confidence_score,
        "education_relevance": item.education_relevance,
        "review_status": item.review_status,
        "share_approved": item.share_approved,
        "canonical_url": item.canonical_url,
        "published_at": item.published_at.isoformat() if item.published_at else None,
        "discovered_at": item.discovered_at.isoformat(),
    }


@router.get("/api/v1/console/recent-intelligence", include_in_schema=False)
async def severity_filtered_recent_intelligence(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: LimitParam = 20,
    severity: SeverityFilter = None,
) -> list[dict[str, object]]:
    del principal
    selected = _selected_severities(severity)
    statement = (
        select(IntelligenceItem)
        .where(IntelligenceItem.severity.in_(selected))
        .order_by(IntelligenceItem.discovered_at.desc())
        .limit(limit)
    )
    items = (await session.scalars(statement)).all()
    return [_serialize(item) for item in items]


@router.get("/api/v1/console/severity-summary", include_in_schema=False)
async def severity_summary(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    severity: SeverityFilter = None,
) -> dict[str, object]:
    del principal
    selected = _selected_severities(severity)
    where = IntelligenceItem.severity.in_(selected)
    since = datetime.now(UTC) - timedelta(hours=24)

    total = int((await session.scalar(select(func.count()).select_from(IntelligenceItem).where(where))) or 0)
    new_last_24h = int(
        (
            await session.scalar(
                select(func.count())
                .select_from(IntelligenceItem)
                .where(where, IntelligenceItem.discovered_at >= since)
            )
        )
        or 0
    )
    average_confidence = float(
        (
            await session.scalar(
                select(func.avg(IntelligenceItem.confidence_score)).where(where)
            )
        )
        or 0.0
    )
    grouped = (
        await session.execute(
            select(IntelligenceItem.severity, func.count())
            .where(where)
            .group_by(IntelligenceItem.severity)
        )
    ).all()
    counts = {_enum_value(key): int(value) for key, value in grouped}
    selected_values = {item.value for item in selected}

    return {
        "selected_severities": [item.value for item in selected],
        "total_intelligence": total,
        "new_last_24h": new_last_24h,
        "average_confidence": average_confidence,
        "severity": {
            name: counts.get(name, 0)
            for name in _SEVERITY_ORDER
            if name in selected_values
        },
    }


_FILTER_CONTROLS = r'''
<div class="severity-filter" data-severity-filter role="group" aria-label="Filter op classificatie">
  <span class="severity-filter-label">Severityfilter</span>
  <label class="severity-choice severity-informational"><input type="checkbox" value="informational" checked> <span aria-hidden="true" class="severity-dot"></span>Informatief</label>
  <label class="severity-choice severity-low"><input type="checkbox" value="low" checked> <span aria-hidden="true" class="severity-dot"></span>Laag</label>
  <label class="severity-choice severity-medium"><input type="checkbox" value="medium" checked> <span aria-hidden="true" class="severity-dot"></span>Middel</label>
  <label class="severity-choice severity-high"><input type="checkbox" value="high" checked> <span aria-hidden="true" class="severity-dot"></span>Hoog</label>
  <label class="severity-choice severity-critical"><input type="checkbox" value="critical" checked> <span aria-hidden="true" class="severity-dot"></span>Kritiek</label>
  <button type="button" class="button secondary severity-reset" data-severity-reset>Alles</button>
</div>
<div class="severity-filter-status status" data-severity-filter-status role="status" aria-live="polite"></div>
'''

_SEVERITY_CSS = r'''
<style id="e1-e2-severity-style">
.severity-filter{display:flex;gap:.55rem;align-items:center;flex-wrap:wrap;margin:0 0 1rem;padding:.8rem 1rem;border:1px solid var(--line);border-radius:12px;background:var(--surface-2)}
.severity-filter-label{font-weight:800;margin-right:.25rem}.severity-choice{display:inline-flex;align-items:center;gap:.35rem;padding:.35rem .55rem;border:1px solid var(--line);border-radius:999px;font-weight:700;cursor:pointer;background:var(--surface)}.severity-choice:focus-within{outline:3px solid currentColor;outline-offset:2px}.severity-choice input{margin:0}.severity-dot{width:.7rem;height:.7rem;border-radius:50%;background:var(--severity-color,#52606d);border:1px solid currentColor}.severity-informational{--severity-color:#667085;color:#475467}.severity-low{--severity-color:#16803c;color:#116329}.severity-medium{--severity-color:#c2410c;color:#9a3412}.severity-high{--severity-color:#b42318;color:#8a1c13}.severity-critical{--severity-color:#7a271a;color:#5f1d14}.severity-filter-status{margin-top:-.45rem;margin-bottom:.8rem}.severity-pill{display:inline-flex;align-items:center;gap:.35rem;border:1px solid currentColor;border-radius:999px;padding:.15rem .5rem;font-weight:800;background:var(--surface)}.severity-pill .severity-dot{flex:0 0 auto}.card.severity-card{border-left:5px solid var(--severity-color,#52606d)}.severity-bar{background:var(--severity-color,#52606d)!important;opacity:.88}.severity-count{font-variant-numeric:tabular-nums}.severity-filter-empty{padding:1rem;border:1px dashed var(--line);border-radius:10px}.kpi-filter-note{display:block;font-size:.75rem;color:var(--muted);margin-top:.2rem}
</style>
'''

_SEVERITY_SCRIPT = r'''
<script src="/ui/severity-experience.js" defer></script>
'''


def extend_console_page(page: str) -> str:
    if 'data-severity-filter' in page:
        return page
    overview_marker = '<div class="kpi-grid">'
    intelligence_marker = '<article class="surface"><h3>Recent ingested</h3>'
    if overview_marker not in page or intelligence_marker not in page:
        raise RuntimeError("canonical Overview/Intelligence markers not found")
    extended = page.replace(overview_marker, _FILTER_CONTROLS + overview_marker, 1)
    extended = extended.replace(intelligence_marker, _FILTER_CONTROLS + intelligence_marker, 1)
    extended = extended.replace("</head>", _SEVERITY_CSS + "</head>", 1)
    extended = extended.replace("</body>", _SEVERITY_SCRIPT + "</body>", 1)
    return extended


_PAGE = extend_console_page(GOVERNANCE_CONSOLE_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def severity_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const order = ['informational', 'low', 'medium', 'high', 'critical'];
  const labels = {
    informational: 'Informatief',
    low: 'Laag',
    medium: 'Middel',
    high: 'Hoog',
    critical: 'Kritiek',
  };
  const selected = new Set(order);
  const originalLoadDashboard = loadDashboard;

  function severityClass(value) {
    const severity = order.includes(String(value || '').toLowerCase()) ? String(value).toLowerCase() : 'informational';
    return `severity-${severity}`;
  }

  function severityLabel(value) {
    const severity = order.includes(String(value || '').toLowerCase()) ? String(value).toLowerCase() : 'informational';
    return labels[severity] || severity;
  }

  function selectedValues() {
    return order.filter((value) => selected.has(value));
  }

  function allSeveritiesSelected() {
    return selected.size === order.length;
  }

  function queryString() {
    return selectedValues().map((value) => `severity=${encodeURIComponent(value)}`).join('&');
  }

  function updateControls(origin) {
    document.querySelectorAll('[data-severity-filter]').forEach((group) => {
      group.querySelectorAll('input[type="checkbox"]').forEach((input) => {
        input.checked = selected.has(input.value);
      });
    });
    const activeLabels = selectedValues().map(severityLabel);
    const message = `Actief severityfilter: ${activeLabels.join(', ')}.`;
    document.querySelectorAll('[data-severity-filter-status]').forEach((target) => { target.textContent = message; });
    if (origin) origin.textContent = message;
  }

  function filteredEmpty(message) {
    return `<div class="severity-filter-empty"><strong>Geen intelligence binnen dit severityfilter.</strong><p class="muted">${esc(message)}</p></div>`;
  }

  function baselineEmpty() {
    return '<div class="empty-state"><strong>Nog geen intelligence ingested.</strong><p>Open Bronnen & catalogus, registreer/activeer een bron en kies “Feed nu laden”.</p><button type="button" class="button secondary" data-view="sources">Open bronnen</button></div>';
  }

  intelCard = function severityIntelCard(item) {
    const severity = String(item.severity || 'informational').toLowerCase();
    const className = severityClass(severity);
    return `<article class="card severity-card ${className}" data-severity="${esc(severity)}"><div class="intel-meta"><span class="severity-pill ${className}"><span aria-hidden="true" class="severity-dot"></span>${esc(severityLabel(severity))}</span><span>${esc(item.source_id || 'onbekende bron')}</span><span>${esc(item.discovered_at ? new Date(item.discovered_at).toLocaleString() : '')}</span></div><strong>${esc(item.title || item.id)}</strong><p>${esc(item.summary || item.description || '')}</p>${item.canonical_url ? `<a href="${esc(item.canonical_url)}" rel="noopener noreferrer">Bron openen</a>` : ''}</article>`;
  };

  function severityBars(target, tableTarget, values) {
    const entries = order.filter((name) => Object.hasOwn(values || {}, name)).map((name) => [name, Number(values[name]) || 0]);
    const total = entries.reduce((sum, [, value]) => sum + Math.max(0, value), 0);
    if (!entries.length || total <= 0) {
      $(target).innerHTML = '<div class="chart-empty"><div><strong>Geen data om te visualiseren</strong><p class="muted">Geen intelligence binnen het actieve severityfilter.</p></div></div>';
      $(tableTarget).innerHTML = '';
      return;
    }
    const max = Math.max(1, ...entries.map(([, value]) => value));
    $(target).innerHTML = entries.map(([name, value]) => `<div class="bar-wrap ${severityClass(name)}"><div class="bar severity-bar" style="height:${value > 0 ? Math.max(8, Math.min(160, (value / max) * 160)) : 2}px" title="${esc(severityLabel(name))}: ${esc(value)}"></div><div class="bar-label">${esc(severityLabel(name))} · ${esc(value)}</div></div>`).join('');
    $(tableTarget).innerHTML = `<table><thead><tr><th>Severity</th><th>Aantal</th></tr></thead><tbody>${entries.map(([name, value]) => `<tr class="${severityClass(name)}"><td><span class="severity-pill ${severityClass(name)}"><span aria-hidden="true" class="severity-dot"></span>${esc(severityLabel(name))}</span></td><td class="severity-count">${esc(value)}</td></tr>`).join('')}</tbody></table>`;
  }

  async function loadSeveritySummary() {
    const suffix = queryString();
    const summary = await api(`/api/v1/console/severity-summary${suffix ? `?${suffix}` : ''}`);
    $('kpi-intel').textContent = summary.total_intelligence ?? 0;
    $('kpi-new').textContent = summary.new_last_24h ?? 0;
    $('kpi-confidence').textContent = `${Number(summary.average_confidence ?? 0).toFixed(1)}%`;
    ['kpi-intel', 'kpi-new', 'kpi-confidence'].forEach((id) => {
      const card = $(id)?.closest('.kpi-card');
      if (card && !card.querySelector('.kpi-filter-note')) card.insertAdjacentHTML('beforeend', '<small class="kpi-filter-note">Gefilterd op geselecteerde severity</small>');
    });
    severityBars('overview-severity-chart', 'overview-severity-table', summary.severity || {});
    return summary;
  }

  loadDashboard = async function severityAwareDashboard() {
    const base = await originalLoadDashboard();
    if (!base.ok) return base;
    try {
      const summary = await loadSeveritySummary();
      return { ...base, data: { ...base.data, ...summary } };
    } catch (error) {
      return { ok: false, error };
    }
  };

  loadRecentIntelligence = async function severityAwareRecent() {
    try {
      const suffix = queryString();
      const rows = await api(`/api/v1/console/recent-intelligence?limit=100${suffix ? `&${suffix}` : ''}`);
      const html = rows.length
        ? rows.map(intelCard).join('')
        : (allSeveritiesSelected() ? baselineEmpty() : filteredEmpty('Pas het filter aan of laad nieuwe brondata.'));
      $('intel-recent').innerHTML = html;
      $('overview-recent').innerHTML = rows.length ? rows.slice(0, 5).map(intelCard).join('') : html;
      $('intel-recent-status').textContent = rows.length
        ? `${rows.length} recente records binnen het actieve severityfilter.`
        : (allSeveritiesSelected()
          ? 'Nog geen canonical intelligence beschikbaar.'
          : 'Geen recente canonical intelligence binnen het actieve severityfilter.');
      return { ok: true, rows };
    } catch (error) {
      $('intel-recent-status').textContent = `Recente intelligence laden mislukt: ${error.message}`;
      return { ok: false, error, rows: [] };
    }
  };

  async function refreshSeverityViews() {
    updateControls();
    const [dashboard, recent] = await Promise.all([loadDashboard(), loadRecentIntelligence()]);
    if (!dashboard.ok || !recent.ok) $('global-status').textContent = 'Severityfilter deels mislukt';
    else if ((dashboard.data.total_intelligence ?? 0) === 0 && recent.rows.length === 0 && allSeveritiesSelected()) {
      $('global-status').textContent = 'Geen intelligence data · bronstatus geladen';
    } else {
      $('global-status').textContent = `Severityfilter bijgewerkt · ${dashboard.data.total_intelligence ?? 0} records`;
    }
  }

  document.querySelectorAll('[data-severity-filter]').forEach((group) => {
    group.addEventListener('change', (event) => {
      const input = event.target.closest('input[type="checkbox"]');
      if (!input) return;
      if (input.checked) selected.add(input.value); else selected.delete(input.value);
      if (!selected.size) {
        selected.add(input.value);
        input.checked = true;
        const filterStatus = group.nextElementSibling;
        if (filterStatus) filterStatus.textContent = 'Minimaal één severity moet geselecteerd blijven.';
        return;
      }
      void refreshSeverityViews();
    });
    group.querySelector('[data-severity-reset]')?.addEventListener('click', () => {
      order.forEach((value) => selected.add(value));
      void refreshSeverityViews();
    });
  });

  const searchForm = $('intel-search');
  searchForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    event.stopImmediatePropagation();
    const query = $('intel-query').value.trim();
    $('intel-status').textContent = 'Zoeken…';
    try {
      const active = selectedValues();
      const serverSeverity = active.length === 1 ? `&severity=${encodeURIComponent(active[0])}` : '';
      const response = await api(`/api/v1/intelligence/search?q=${encodeURIComponent(query)}${serverSeverity}`);
      const rows = Array.isArray(response) ? response : (response.items || response.results || []);
      const filtered = rows.filter((row) => selected.has(String(row.severity || 'informational').toLowerCase()));
      $('intel-results').innerHTML = filtered.length ? filtered.map(intelCard).join('') : filteredEmpty('Geen zoekresultaten binnen het actieve severityfilter.');
      $('intel-status').textContent = `${filtered.length} resultaten binnen het actieve severityfilter.`;
    } catch (error) {
      $('intel-status').textContent = `Zoeken mislukt: ${error.message}`;
    }
  }, true);

  updateControls();
  void refreshSeverityViews();
})();
'''


@router.get("/ui/severity-experience.js", include_in_schema=False)
def severity_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})
