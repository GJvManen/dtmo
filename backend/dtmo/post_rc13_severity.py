from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.connectors.state import ConnectorRuntimeState
from dtmo.intelligence.model import IntelligenceSeverity
from dtmo.persistence.models import IntelligenceItem
from dtmo.rc13_governance import _PAGE as GOVERNANCE_CONSOLE_PAGE

router = APIRouter()

SEVERITY_VALUES: tuple[str, ...] = tuple(item.value for item in IntelligenceSeverity)


def _severity_where(severity: IntelligenceSeverity | None):  # type: ignore[no-untyped-def]
    return IntelligenceItem.severity == severity if severity is not None else None


async def _intelligence_group_counts(
    session: AsyncSession,
    column,  # type: ignore[no-untyped-def]
    severity: IntelligenceSeverity | None,
) -> dict[str, int]:
    statement = select(column, func.count()).select_from(IntelligenceItem).group_by(column)
    condition = _severity_where(severity)
    if condition is not None:
        statement = statement.where(condition)
    rows = (await session.execute(statement)).all()
    return {
        str(value.value if hasattr(value, "value") else value): int(count)
        for value, count in rows
    }


async def _connector_health_counts(session: AsyncSession) -> dict[str, int]:
    rows = (
        await session.execute(
            select(ConnectorRuntimeState.health_status, func.count()).group_by(
                ConnectorRuntimeState.health_status
            )
        )
    ).all()
    return {
        str(value.value if hasattr(value, "value") else value): int(count)
        for value, count in rows
    }


async def _filtered_seven_day_trend(
    session: AsyncSession,
    severity: IntelligenceSeverity | None,
) -> dict[str, int]:
    today = datetime.now(UTC).date()
    first_day = today - timedelta(days=6)
    counts = {
        (first_day + timedelta(days=offset)).isoformat(): 0 for offset in range(7)
    }
    statement = select(IntelligenceItem.discovered_at).where(
        IntelligenceItem.discovered_at
        >= datetime.combine(first_day, datetime.min.time(), tzinfo=UTC)
    )
    condition = _severity_where(severity)
    if condition is not None:
        statement = statement.where(condition)
    discovered = (await session.scalars(statement)).all()
    for value in discovered:
        if value is None:
            continue
        key = value.astimezone(UTC).date().isoformat()
        if key in counts:
            counts[key] += 1
    return counts


def _apply_severity(statement, severity: IntelligenceSeverity | None):  # type: ignore[no-untyped-def]
    condition = _severity_where(severity)
    return statement.where(condition) if condition is not None else statement


@router.get("/api/v1/dashboards/summary")
async def filtered_dashboard_summary(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    severity: IntelligenceSeverity | None = Query(default=None),
) -> dict[str, object]:
    """Return one internally consistent dashboard slice for the selected severity.

    Connector health is intentionally operational and therefore remains unfiltered.
    All intelligence-derived KPI, trend, source and review aggregates use the same
    canonical PostgreSQL severity predicate.
    """
    del principal
    total_statement = _apply_severity(select(func.count(IntelligenceItem.id)), severity)
    total = int((await session.scalar(total_statement)) or 0)

    recent_cutoff = datetime.now(UTC) - timedelta(hours=24)
    recent_statement = select(func.count(IntelligenceItem.id)).where(
        IntelligenceItem.discovered_at >= recent_cutoff
    )
    recent_statement = _apply_severity(recent_statement, severity)
    recent = int((await session.scalar(recent_statement)) or 0)

    confidence_statement = _apply_severity(
        select(func.avg(IntelligenceItem.confidence_score)), severity
    )
    average_confidence = float((await session.scalar(confidence_statement)) or 0.0)

    severity_counts = await _intelligence_group_counts(
        session, IntelligenceItem.severity, severity
    )
    review_status = await _intelligence_group_counts(
        session, IntelligenceItem.review_status, severity
    )
    sources = await _intelligence_group_counts(session, IntelligenceItem.source_id, severity)
    connector_health = await _connector_health_counts(session)
    trend = await _filtered_seven_day_trend(session, severity)

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "severity_filter": severity.value if severity is not None else None,
        "severity_values": list(SEVERITY_VALUES),
        "total_intelligence": total,
        "new_last_24h": recent,
        "average_confidence": round(average_confidence, 1),
        "severity": severity_counts,
        "review_status": review_status,
        "sources": sources,
        "connector_health": connector_health,
        "connector_health_filter_scope": "operational-unfiltered",
        "intelligence_trend_7d": trend,
        "publication_boundary": "human-review-and-separate-share-approval-required",
    }


def _enum_value(value: object) -> str:
    return str(getattr(value, "value", value))


@router.get("/api/v1/console/recent-intelligence")
async def filtered_recent_console_intelligence(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=20, ge=1, le=100),
    severity: IntelligenceSeverity | None = Query(default=None),
) -> list[dict[str, object]]:
    """Return canonical recent intelligence with the shared severity predicate."""
    del principal
    statement = select(IntelligenceItem).order_by(IntelligenceItem.discovered_at.desc())
    statement = _apply_severity(statement, severity).limit(limit)
    items = (await session.scalars(statement)).all()
    return [
        {
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
        for item in items
    ]


_OVERVIEW_FILTER = r'''
<section class="severity-filter-panel surface" aria-labelledby="overview-severity-filter-title">
  <div>
    <h3 id="overview-severity-filter-title">Severity filter</h3>
    <p class="muted">KPI's, intelligence-trend, severitygrafiek en recente intelligence gebruiken hetzelfde filter. Connector health blijft een operationele, ongefilterde status.</p>
  </div>
  <label for="overview-severity-filter">Toon severity
    <select id="overview-severity-filter" data-severity-filter>
      <option value="all">Alle severities</option>
      <option value="informational">Informational</option>
      <option value="low">Low</option>
      <option value="medium">Medium</option>
      <option value="high">High</option>
      <option value="critical">Critical</option>
    </select>
  </label>
  <div class="severity-legend" aria-label="Severity kleurlegenda">
    <span class="severity-chip severity-informational">Informational</span>
    <span class="severity-chip severity-low">Low</span>
    <span class="severity-chip severity-medium">Medium</span>
    <span class="severity-chip severity-high">High</span>
    <span class="severity-chip severity-critical">Critical</span>
  </div>
  <p class="severity-filter-state" data-severity-filter-state role="status" aria-live="polite"></p>
</section>
'''

_INTELLIGENCE_FILTER = r'''
<section class="severity-filter-panel surface" aria-labelledby="intelligence-severity-filter-title">
  <div>
    <h3 id="intelligence-severity-filter-title">Severity filter</h3>
    <p class="muted">Hetzelfde filter geldt voor Recent ingested en bestaande governed search. Frameworkmapping blijft afzonderlijk en wordt niet afgeleid uit severity.</p>
  </div>
  <label for="intelligence-severity-filter">Toon severity
    <select id="intelligence-severity-filter" data-severity-filter>
      <option value="all">Alle severities</option>
      <option value="informational">Informational</option>
      <option value="low">Low</option>
      <option value="medium">Medium</option>
      <option value="high">High</option>
      <option value="critical">Critical</option>
    </select>
  </label>
  <p class="severity-filter-state" data-severity-filter-state role="status" aria-live="polite"></p>
</section>
'''

_STYLE_TAG = '<link rel="stylesheet" href="/ui/post-rc13-severity.css">'
_SCRIPT_TAG = '<script src="/ui/post-rc13-severity.js" defer></script>'


def extend_console_page(page: str) -> str:
    if _STYLE_TAG not in page:
        page = page.replace("</head>", _STYLE_TAG + "</head>", 1)

    overview_marker = '<div class="kpi-grid">'
    if overview_marker not in page:
        raise RuntimeError("canonical Overview KPI marker not found")
    page = page.replace(overview_marker, _OVERVIEW_FILTER + overview_marker, 1)

    intelligence_marker = '<article class="surface"><h3>Recent ingested</h3>'
    if intelligence_marker not in page:
        raise RuntimeError("canonical Intelligence recent marker not found")
    page = page.replace(
        intelligence_marker,
        _INTELLIGENCE_FILTER + intelligence_marker,
        1,
    )

    if _SCRIPT_TAG not in page:
        page = page.replace("</body>", _SCRIPT_TAG + "</body>", 1)
    return page


_PAGE = extend_console_page(GOVERNANCE_CONSOLE_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def post_rc13_severity_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_CSS = r'''
.severity-filter-panel{display:grid;grid-template-columns:minmax(220px,1fr) minmax(190px,260px);gap:.75rem 1rem;align-items:end;margin:0 0 1rem}.severity-filter-panel h3{margin:0}.severity-filter-panel p{margin:.25rem 0 0}.severity-filter-panel label{font-weight:700}.severity-filter-panel select{width:100%;margin-top:.25rem}.severity-legend{grid-column:1/-1;display:flex;gap:.45rem;flex-wrap:wrap}.severity-filter-state{grid-column:1/-1;min-height:1.2rem;font-size:.9rem}.severity-chip,.intel-meta .severity-chip{display:inline-flex;align-items:center;gap:.35rem;border:1px solid currentColor;border-radius:999px;padding:.18rem .55rem;font-weight:700}.severity-chip::before,.severity-bar::before{content:"";display:inline-block;width:.55rem;height:.55rem;border-radius:50%;background:currentColor}.severity-informational{color:#334e68;background:#edf2f7}.severity-low{color:#176b3a;background:#e7f6ec}.severity-medium{color:#7a4b00;background:#fff3cd}.severity-high{color:#a61b1b;background:#fde8e8}.severity-critical{color:#fff;background:#651426;border-color:#651426}.severity-critical::before{background:#fff}.severity-bar{border:1px solid currentColor;border-radius:6px 6px 0 0;opacity:.88}.severity-bar.severity-informational{background:#9fb3c8}.severity-bar.severity-low{background:#2f9e5b}.severity-bar.severity-medium{background:#d99a00}.severity-bar.severity-high{background:#cf3030}.severity-bar.severity-critical{background:#651426}.severity-bar-label{display:flex;justify-content:center;gap:.25rem;align-items:center}.severity-dot{display:inline-block;width:.5rem;height:.5rem;border-radius:50%;background:currentColor}@media(max-width:720px){.severity-filter-panel{grid-template-columns:1fr}.severity-legend,.severity-filter-state{grid-column:1}}
'''


@router.get("/ui/post-rc13-severity.css", include_in_schema=False)
def post_rc13_severity_css() -> Response:
    return Response(_CSS, media_type="text/css", headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const values = ['informational', 'low', 'medium', 'high', 'critical'];
  const labels = {
    all: 'Alle severities',
    informational: 'Informational',
    low: 'Low',
    medium: 'Medium',
    high: 'High',
    critical: 'Critical',
  };
  const apiPrefixes = [
    '/api/v1/dashboards/summary',
    '/api/v1/console/recent-intelligence',
    '/api/v1/intelligence/search',
  ];
  let selected = sessionStorage.getItem('dtmo.severityFilter') || 'all';
  if (selected !== 'all' && !values.includes(selected)) selected = 'all';

  function severityLabel(value) {
    return labels[value] || labels.all;
  }

  function syncControls() {
    document.querySelectorAll('[data-severity-filter]').forEach((control) => {
      control.value = selected;
    });
    document.querySelectorAll('[data-severity-filter-state]').forEach((target) => {
      target.textContent = selected === 'all'
        ? 'Geen severityfilter actief.'
        : `Actief filter: ${severityLabel(selected)}.`;
    });
  }

  function withSeverity(url) {
    if (selected === 'all' || !apiPrefixes.some((prefix) => url.startsWith(prefix))) return url;
    const parsed = new URL(url, window.location.origin);
    parsed.searchParams.set('severity', selected);
    return `${parsed.pathname}${parsed.search}`;
  }

  const baseApi = api;
  api = async function severityAwareApi(url, options = {}) {
    return baseApi(withSeverity(url), options);
  };

  intelCard = function severityIntelCard(item) {
    const value = values.includes(String(item.severity || '').toLowerCase())
      ? String(item.severity).toLowerCase()
      : 'informational';
    return `<article class="card"><div class="intel-meta"><span class="severity-chip severity-${esc(value)}" aria-label="Severity ${esc(severityLabel(value))}">${esc(severityLabel(value))}</span><span>${esc(item.source_id || 'onbekende bron')}</span><span>${esc(item.discovered_at ? new Date(item.discovered_at).toLocaleString() : '')}</span></div><strong>${esc(item.title || item.id)}</strong><p>${esc(item.summary || item.description || '')}</p>${item.canonical_url ? `<a href="${esc(item.canonical_url)}" rel="noopener noreferrer">Bron openen</a>` : ''}</article>`;
  };

  function severityBars(target, tableTarget, data, emptyMessage) {
    const rows = values
      .filter((key) => Object.prototype.hasOwnProperty.call(data || {}, key))
      .map((key) => [key, Number(data[key]) || 0]);
    const total = rows.reduce((sum, [, value]) => sum + Math.max(0, value), 0);
    if (!rows.length || total <= 0) {
      $(target).innerHTML = `<div class="chart-empty"><div><strong>Geen data om te visualiseren</strong><p class="muted">${esc(emptyMessage)}</p></div></div>`;
      $(tableTarget).innerHTML = '';
      return false;
    }
    const max = Math.max(1, ...rows.map(([, value]) => value));
    $(target).innerHTML = rows.map(([key, value]) => `<div class="bar-wrap"><div class="bar severity-bar severity-${esc(key)}" style="height:${value > 0 ? Math.max(8, Math.min(160, (value / max) * 160)) : 2}px" title="${esc(severityLabel(key))}: ${esc(value)}"></div><div class="bar-label severity-bar-label"><span class="severity-dot severity-${esc(key)}" aria-hidden="true"></span>${esc(severityLabel(key))}</div></div>`).join('');
    $(tableTarget).innerHTML = `<table><thead><tr><th>Severity</th><th>Aantal</th></tr></thead><tbody>${rows.map(([key, value]) => `<tr><td><span class="severity-chip severity-${esc(key)}">${esc(severityLabel(key))}</span></td><td>${esc(value)}</td></tr>`).join('')}</tbody></table>`;
    return true;
  }

  const baseBars = bars;
  bars = function severityAwareBars(target, tableTarget, data, emptyMessage) {
    if (target === 'overview-severity-chart') {
      return severityBars(
        target,
        tableTarget,
        data,
        selected === 'all'
          ? emptyMessage
          : `Geen intelligence met severity ${severityLabel(selected)}.`,
      );
    }
    return baseBars(target, tableTarget, data, emptyMessage);
  };

  const baseLoadRecentIntelligence = loadRecentIntelligence;
  loadRecentIntelligence = async function severityAwareRecentIntelligence() {
    const result = await baseLoadRecentIntelligence();
    if (selected !== 'all' && result.ok) {
      if (!result.rows.length) {
        const empty = `<div class="empty-state"><strong>Geen recente intelligence met severity ${esc(severityLabel(selected))}.</strong><p>Pas het severityfilter aan of laad aanvullende bronnen.</p></div>`;
        $('intel-recent').innerHTML = empty;
        $('overview-recent').innerHTML = empty;
        $('intel-recent-status').textContent = `Geen recente records met severity ${severityLabel(selected)}.`;
      } else {
        $('intel-recent-status').textContent = `${result.rows.length} recente records met severity ${severityLabel(selected)} geladen.`;
      }
    }
    return result;
  };

  const baseRefreshAll = refreshAll;
  refreshAll = async function severityAwareRefreshAll(options = {}) {
    const result = await baseRefreshAll(options);
    if (selected !== 'all' && result.ok) {
      const total = Number(result.dashboard.data?.total_intelligence || 0);
      $('global-status').textContent = total === 0
        ? `Geen intelligence voor filter ${severityLabel(selected)} · bronstatus geladen`
        : `Bijgewerkt · ${total} ${severityLabel(selected)} intelligence record${total === 1 ? '' : 's'}`;
    }
    return result;
  };

  const results = $('intel-results');
  if (results) {
    new MutationObserver(() => {
      if (selected === 'all') return;
      const empty = results.querySelector('.empty-state');
      if (empty && empty.textContent.trim() === 'Geen zoekresultaten.') {
        empty.textContent = `Geen zoekresultaten met severity ${severityLabel(selected)}.`;
      }
      const status = $('intel-status');
      if (status && /^\d+ resultaten\.$/.test(status.textContent.trim())) {
        status.textContent = `${status.textContent.trim()} Filter: ${severityLabel(selected)}.`;
      }
    }).observe(results, {childList: true, subtree: true});
  }

  async function applySeverity(nextValue) {
    selected = nextValue === 'all' || values.includes(nextValue) ? nextValue : 'all';
    sessionStorage.setItem('dtmo.severityFilter', selected);
    syncControls();
    await Promise.all([loadDashboard(), loadRecentIntelligence()]);
    const query = $('intel-query')?.value.trim() || '';
    if (query.length >= 2) $('intel-search')?.requestSubmit();
    if (selected === 'all') {
      $('global-status').textContent = 'Severityfilter gewist · dashboard en intelligence vernieuwd';
    } else {
      $('global-status').textContent = `Severityfilter ${severityLabel(selected)} toegepast`;
    }
  }

  document.addEventListener('change', (event) => {
    const control = event.target instanceof Element
      ? event.target.closest('[data-severity-filter]')
      : null;
    if (control) void applySeverity(control.value);
  });

  syncControls();
  void applySeverity(selected);
})();
'''


@router.get("/ui/post-rc13-severity.js", include_in_schema=False)
def post_rc13_severity_script() -> Response:
    return Response(
        _SCRIPT,
        media_type="application/javascript",
        headers={"Cache-Control": "no-store"},
    )
