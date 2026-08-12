from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.api.routes import get_session
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.intelligence.model import IntelligenceSeverity
from dtmo.persistence.models import IntelligenceItem
from dtmo.severity_experience import _PAGE as SEVERITY_CONSOLE_PAGE
from dtmo.severity_experience import _enum_value, _selected_severities

router = APIRouter()

SeverityFilter = Annotated[list[str] | None, Query()]
TrendWindow = Annotated[str, Query(pattern=r"^(24h|7d|30d)$")]

_TREND_CONFIG: dict[str, tuple[int, timedelta, str]] = {
    "24h": (24, timedelta(hours=1), "uur"),
    "7d": (7, timedelta(days=1), "dag"),
    "30d": (30, timedelta(days=1), "dag"),
}


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _trend_change_percent(current: int, previous: int) -> float | None:
    if previous == 0:
        return 0.0 if current == 0 else None
    return round(((current - previous) / previous) * 100.0, 1)


def _share(elevated: int, total: int) -> float:
    return round((elevated / total) * 100.0, 1) if total else 0.0


def _build_trend_payload(
    observations: list[tuple[datetime, object]],
    selected: tuple[IntelligenceSeverity, ...],
    window: str,
    now: datetime,
) -> dict[str, object]:
    bucket_count, bucket_size, bucket_unit = _TREND_CONFIG[window]
    end = _utc(now)
    duration = bucket_size * bucket_count
    start = end - duration
    previous_start = start - duration

    selected_values = [item.value for item in selected]
    bucket_totals = [0 for _ in range(bucket_count)]
    bucket_severity = [
        {severity: 0 for severity in selected_values}
        for _ in range(bucket_count)
    ]
    current_total = 0
    previous_total = 0
    current_elevated = 0
    previous_elevated = 0
    elevated_values = {
        IntelligenceSeverity.HIGH.value,
        IntelligenceSeverity.CRITICAL.value,
    }

    for discovered_at, severity_raw in observations:
        timestamp = _utc(discovered_at)
        severity = _enum_value(severity_raw)
        if severity not in selected_values or timestamp < previous_start or timestamp >= end:
            continue
        elevated = severity in elevated_values
        if timestamp >= start:
            current_total += 1
            if elevated:
                current_elevated += 1
            index = int((timestamp - start) // bucket_size)
            if 0 <= index < bucket_count:
                bucket_totals[index] += 1
                bucket_severity[index][severity] += 1
        else:
            previous_total += 1
            if elevated:
                previous_elevated += 1

    buckets: list[dict[str, object]] = []
    for index in range(bucket_count):
        bucket_start = start + (bucket_size * index)
        label = bucket_start.strftime("%H:%M") if window == "24h" else bucket_start.strftime("%d %b")
        buckets.append(
            {
                "start": bucket_start.isoformat(),
                "label": label,
                "total": bucket_totals[index],
                "severity": bucket_severity[index],
                "elevated_share_percent": _share(
                    sum(bucket_severity[index].get(name, 0) for name in elevated_values),
                    bucket_totals[index],
                ),
            }
        )

    current_share = _share(current_elevated, current_total)
    previous_share = _share(previous_elevated, previous_total)
    return {
        "window": window,
        "bucket_unit": bucket_unit,
        "generated_at": end.isoformat(),
        "selected_severities": selected_values,
        "buckets": buckets,
        "comparison": {
            "current_total": current_total,
            "previous_total": previous_total,
            "volume_delta": current_total - previous_total,
            "volume_change_percent": _trend_change_percent(current_total, previous_total),
            "current_elevated": current_elevated,
            "previous_elevated": previous_elevated,
            "current_elevated_share_percent": current_share,
            "previous_elevated_share_percent": previous_share,
            "elevated_share_delta_percentage_points": round(current_share - previous_share, 1),
        },
    }


@router.get("/api/v1/console/trends", include_in_schema=False)
async def intelligence_trends(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
    session: Annotated[AsyncSession, Depends(get_session)],
    window: TrendWindow = "7d",
    severity: SeverityFilter = None,
) -> dict[str, object]:
    del principal
    selected = _selected_severities(severity)
    now = datetime.now(UTC)
    bucket_count, bucket_size, _ = _TREND_CONFIG[window]
    previous_start = now - (bucket_size * bucket_count * 2)
    rows = (
        await session.execute(
            select(IntelligenceItem.discovered_at, IntelligenceItem.severity).where(
                IntelligenceItem.discovered_at >= previous_start,
                IntelligenceItem.severity.in_(selected),
            )
        )
    ).all()
    observations = [
        (discovered_at, severity_value)
        for discovered_at, severity_value in rows
        if discovered_at is not None
    ]
    return _build_trend_payload(observations, selected, window, now)


_OVERVIEW_OLD = (
    '<article class="surface"><h3>Intelligence trend — 7 dagen</h3>'
    '<div id="overview-trend-chart" class="chart"></div>'
    '<div id="overview-trend-table"></div></article>'
)

_WINDOW_CONTROLS = r'''
<div class="trend-window-controls" role="group" aria-label="Trendperiode">
  <button type="button" class="button secondary" data-trend-window="24h" aria-pressed="false">24 uur</button>
  <button type="button" class="button secondary" data-trend-window="7d" aria-pressed="true">7 dagen</button>
  <button type="button" class="button secondary" data-trend-window="30d" aria-pressed="false">30 dagen</button>
</div>
'''

_OVERVIEW_NEW = (
    '<article class="surface" data-trend-surface="overview">'
    '<div class="trend-heading"><div><h3>Intelligence trend</h3>'
    '<p class="muted">Volume en severitymix over een selecteerbaar tijdvenster.</p></div>'
    + _WINDOW_CONTROLS
    + '</div><div id="overview-trend-stats" class="trend-stats"></div>'
    '<div id="overview-trend-chart" class="trend-columns"></div>'
    '<div id="overview-trend-table" class="trend-table-wrap"></div>'
    '<p class="trend-note">Volumeontwikkeling en het aandeel hoog/kritiek worden afzonderlijk weergegeven; '
    'DTMO leidt hieruit geen autonome risicoscore af.</p></article>'
)

_ANALYTICS_PANEL = (
    '<article class="surface" data-trend-surface="analytics">'
    '<div class="trend-heading"><div><h3>Trendanalyse</h3>'
    '<p class="muted">Vergelijk 24 uur, 7 dagen en 30 dagen met de direct voorafgaande gelijke periode.</p></div>'
    + _WINDOW_CONTROLS
    + '</div><div id="analytics-trend-stats" class="trend-stats"></div>'
    '<div id="analytics-trend-chart" class="trend-columns"></div>'
    '<div id="analytics-trend-table" class="trend-table-wrap"></div>'
    '<p class="trend-note">Een volumestijging is niet automatisch een risicostijging. '
    'Het aandeel hoog/kritiek wordt daarom als aparte severitymix-indicator getoond.</p></article>'
)

_CSS = r'''
<style id="e4-analytics-style">
.trend-heading{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;flex-wrap:wrap}
.trend-window-controls{display:flex;gap:.35rem;flex-wrap:wrap}
.trend-window-controls .button[aria-pressed="true"]{box-shadow:0 0 0 2px currentColor inset;font-weight:800}
.trend-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.65rem;margin:.8rem 0}
.trend-stat{border:1px solid var(--line);border-radius:10px;padding:.7rem;background:var(--surface-2)}
.trend-stat strong{display:block;font-size:1.35rem;font-variant-numeric:tabular-nums}
.trend-columns{display:flex;align-items:flex-end;gap:.28rem;min-height:190px;padding:.75rem 0;overflow-x:auto}
.trend-column{display:flex;flex:1 0 20px;min-width:20px;max-width:54px;flex-direction:column;justify-content:flex-end;align-items:stretch;min-height:175px}
.trend-stack{height:150px;display:flex;flex-direction:column-reverse;justify-content:flex-start;border-bottom:1px solid var(--line)}
.trend-segment{width:100%;min-height:0;background:var(--severity-color,#667085)}
.trend-column-label{font-size:.66rem;text-align:center;white-space:nowrap;margin-top:.3rem;color:var(--muted)}
.trend-table-wrap{overflow-x:auto}.trend-note{font-size:.82rem;color:var(--muted)}
</style>
'''

_SCRIPT_TAG = '<script src="/ui/analytics-experience.js" defer></script>'


def extend_console_page(page: str) -> str:
    if 'data-trend-surface="analytics"' in page:
        return page
    if _OVERVIEW_OLD not in page:
        raise RuntimeError("canonical Overview trend marker not found")
    analytics_marker = '<p class="eyebrow">Native console summary</p>'
    if analytics_marker not in page:
        raise RuntimeError("canonical Analytics marker not found")
    extended = page.replace(_OVERVIEW_OLD, _OVERVIEW_NEW, 1)
    extended = extended.replace(analytics_marker, _ANALYTICS_PANEL + analytics_marker, 1)
    extended = extended.replace("</head>", _CSS + "</head>", 1)
    extended = extended.replace("</body>", _SCRIPT_TAG + "</body>", 1)
    return extended


_PAGE = extend_console_page(SEVERITY_CONSOLE_PAGE)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/ui/console", response_class=HTMLResponse, include_in_schema=False)
def analytics_console() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "no-store"})


_SCRIPT = r'''
(() => {
  const severityOrder = ['informational', 'low', 'medium', 'high', 'critical'];
  const severityLabels = {informational:'Informatief',low:'Laag',medium:'Middel',high:'Hoog',critical:'Kritiek'};
  let trendWindow = '7d';

  function selectedSeverityQuery() {
    const group = document.querySelector('[data-severity-filter]');
    if (!group) return '';
    return [...group.querySelectorAll('input[type="checkbox"]')]
      .filter((input) => input.checked)
      .map((input) => `severity=${encodeURIComponent(input.value)}`)
      .join('&');
  }

  function severityClass(value) {
    const severity = severityOrder.includes(String(value || '').toLowerCase()) ? String(value).toLowerCase() : 'informational';
    return `severity-${severity}`;
  }

  function severityLabel(value) {
    const severity = String(value || '').toLowerCase();
    return severityLabels[severity] || severity;
  }

  function windowLabel() {
    return trendWindow === '24h' ? '24 uur' : (trendWindow === '30d' ? '30 dagen' : '7 dagen');
  }

  function signed(value, suffix='') {
    const number = Number(value || 0);
    return `${number > 0 ? '+' : ''}${number}${suffix}`;
  }

  function renderStats(target, comparison) {
    const change = comparison.volume_change_percent;
    const volumeChange = change === null ? (comparison.current_total > 0 ? 'nieuw t.o.v. 0' : '0%') : signed(change, '%');
    $(target).innerHTML = `
      <article class="trend-stat"><span>Huidige ${esc(windowLabel())}</span><strong>${esc(comparison.current_total ?? 0)}</strong><small>meldingen</small></article>
      <article class="trend-stat"><span>Vorige gelijke periode</span><strong>${esc(comparison.previous_total ?? 0)}</strong><small>meldingen</small></article>
      <article class="trend-stat"><span>Volumeverandering</span><strong>${esc(volumeChange)}</strong><small>${esc(signed(comparison.volume_delta ?? 0))} meldingen</small></article>
      <article class="trend-stat"><span>Aandeel hoog/kritiek</span><strong>${esc(Number(comparison.current_elevated_share_percent ?? 0).toFixed(1))}%</strong><small>${esc(signed(comparison.elevated_share_delta_percentage_points ?? 0,' pp'))} t.o.v. vorige periode</small></article>`;
  }

  function renderChart(target, tableTarget, payload) {
    const buckets = payload.buckets || [];
    const max = Math.max(1, ...buckets.map((bucket) => Number(bucket.total || 0)));
    const labelEvery = buckets.length > 20 ? 5 : (buckets.length > 10 ? 2 : 1);
    $(target).innerHTML = buckets.map((bucket,index) => {
      const parts = severityOrder.map((name) => {
        const count = Number(bucket.severity?.[name] || 0);
        const height = count > 0 ? Math.max(2,(count/max)*150) : 0;
        return `<span class="trend-segment ${severityClass(name)}" style="height:${height}px" title="${esc(severityLabel(name))}: ${esc(count)}"></span>`;
      }).join('');
      const label = index % labelEvery === 0 || index === buckets.length - 1 ? bucket.label : '·';
      return `<div class="trend-column" title="${esc(bucket.label)} · ${esc(bucket.total)}"><div class="trend-stack">${parts}</div><div class="trend-column-label">${esc(label)}</div></div>`;
    }).join('') || '<div class="chart-empty"><strong>Geen trenddata</strong></div>';

    const rows = buckets.map((bucket) => `<tr><td>${esc(bucket.label)}</td><td>${esc(bucket.total)}</td><td>${esc(bucket.severity?.informational||0)}</td><td>${esc(bucket.severity?.low||0)}</td><td>${esc(bucket.severity?.medium||0)}</td><td>${esc(bucket.severity?.high||0)}</td><td>${esc(bucket.severity?.critical||0)}</td><td>${esc(Number(bucket.elevated_share_percent||0).toFixed(1))}%</td></tr>`).join('');
    $(tableTarget).innerHTML = `<table><thead><tr><th>Periode</th><th>Totaal</th><th>Informatief</th><th>Laag</th><th>Middel</th><th>Hoog</th><th>Kritiek</th><th>Hoog/kritiek</th></tr></thead><tbody>${rows||'<tr><td colspan="8">Geen data</td></tr>'}</tbody></table>`;
  }

  async function loadTrend() {
    const severity = selectedSeverityQuery();
    const payload = await api(`/api/v1/console/trends?window=${encodeURIComponent(trendWindow)}${severity?`&${severity}`:''}`);
    ['overview','analytics'].forEach((prefix) => {
      if (!$(`${prefix}-trend-chart`)) return;
      renderStats(`${prefix}-trend-stats`,payload.comparison||{});
      renderChart(`${prefix}-trend-chart`,`${prefix}-trend-table`,payload);
    });
    document.querySelectorAll('[data-trend-window]').forEach((button) => {
      button.setAttribute('aria-pressed',String(button.dataset.trendWindow===trendWindow));
    });
  }

  document.querySelectorAll('[data-trend-window]').forEach((button) => {
    button.addEventListener('click',() => {
      const requested = button.dataset.trendWindow;
      if (!['24h','7d','30d'].includes(requested)) return;
      trendWindow = requested;
      void loadTrend().catch((error) => {$('global-status').textContent=`Trend laden mislukt: ${error.message}`;});
    });
  });

  document.querySelectorAll('[data-severity-filter]').forEach((group) => {
    group.addEventListener('change',() => {
      void loadTrend().catch((error) => {$('global-status').textContent=`Trend laden mislukt: ${error.message}`;});
    });
  });
  document.querySelectorAll('[data-severity-reset]').forEach((button) => {
    button.addEventListener('click',() => {
      queueMicrotask(() => void loadTrend().catch((error) => {$('global-status').textContent=`Trend laden mislukt: ${error.message}`;}));
    });
  });

  void loadTrend().catch((error) => {$('global-status').textContent=`Trend laden mislukt: ${error.message}`;});
})();
'''


@router.get("/ui/analytics-experience.js", include_in_schema=False)
def analytics_script() -> Response:
    return Response(_SCRIPT, media_type="application/javascript", headers={"Cache-Control": "no-store"})
