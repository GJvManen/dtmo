from __future__ import annotations

import re
from dataclasses import dataclass
from threading import Lock

import httpx
from prometheus_client import Counter, Gauge

from dtmo.logging import correlation_id, get_logger, resolve_correlation_id

SEARCH_HEALTH_CHECKS = Counter(
    "dtmo_search_health_checks_total",
    "Observed bounded OpenSearch cluster health outcomes",
    ["cluster", "status"],
)
SEARCH_HEALTH_UNHEALTHY_STREAK = Gauge(
    "dtmo_search_health_unhealthy_streak",
    "Consecutive red or unreachable OpenSearch health outcomes",
    ["cluster"],
)
SEARCH_HEALTH_RECOVERY_STREAK = Gauge(
    "dtmo_search_health_recovery_streak",
    "Consecutive green/yellow outcomes while a search-health alert is active",
    ["cluster"],
)
SEARCH_HEALTH_ALERT_ACTIVE = Gauge(
    "dtmo_search_health_alert_active",
    "Whether the bounded search-health alert is active",
    ["cluster"],
)
SEARCH_HEALTH_ALERT_TRANSITIONS = Counter(
    "dtmo_search_health_alert_transitions_total",
    "Search-health alert state transitions",
    ["cluster", "transition"],
)

_CLUSTER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}$")
_ACTION = (
    "Inspect OpenSearch cluster health, node availability, shard allocation and recent changes; "
    "avoid treating incomplete search results as authoritative until health recovers."
)


def _current_correlation(value: str | None) -> str:
    current = value or correlation_id.get()
    return resolve_correlation_id(None) if current == "-" else current


@dataclass(frozen=True, slots=True)
class SearchHealthAlertSignal:
    cluster: str
    health_status: str
    state: str
    transitioned: bool
    correlation_id: str
    unhealthy_streak: int
    recovery_streak: int
    action: str
    publish_approved: bool = False


class SearchHealthAlertManager:
    """Observe only bounded cluster-health state, never search data or query material."""

    def __init__(self, *, raise_after: int = 2, clear_after: int = 2) -> None:
        if raise_after < 1 or clear_after < 1:
            raise ValueError("search-health thresholds must be positive")
        self.raise_after = raise_after
        self.clear_after = clear_after
        self._unhealthy: dict[str, int] = {}
        self._recovery: dict[str, int] = {}
        self._active: set[str] = set()
        self._lock = Lock()
        self.log = get_logger("search.alerts")

    def observe(self, cluster: str, *, health_status: str, correlation: str | None = None) -> SearchHealthAlertSignal:
        name = cluster.strip()
        if not _CLUSTER.fullmatch(name):
            raise ValueError("cluster must be a bounded operational identifier")
        status = health_status.strip().lower()
        if status not in {"green", "yellow", "red", "unreachable"}:
            raise ValueError("health_status must be green, yellow, red or unreachable")

        current = _current_correlation(correlation)
        SEARCH_HEALTH_CHECKS.labels(name, status).inc()
        unhealthy = status in {"red", "unreachable"}

        with self._lock:
            was_active = name in self._active
            bad = self._unhealthy.get(name, 0)
            recovery = self._recovery.get(name, 0)
            transitioned = False

            if unhealthy:
                bad += 1
                recovery = 0
                self._unhealthy[name] = bad
                self._recovery[name] = 0
                SEARCH_HEALTH_UNHEALTHY_STREAK.labels(name).set(bad)
                SEARCH_HEALTH_RECOVERY_STREAK.labels(name).set(0)
                if was_active or bad >= self.raise_after:
                    self._active.add(name)
                    state = "active"
                    SEARCH_HEALTH_ALERT_ACTIVE.labels(name).set(1)
                    if not was_active:
                        transitioned = True
                        SEARCH_HEALTH_ALERT_TRANSITIONS.labels(name, "raised").inc()
                        event = "search_health_alert_raised"
                    else:
                        event = "search_health_alert_active"
                    self.log.warning(
                        event,
                        cluster=name,
                        health_status=status,
                        correlation_id=current,
                        severity="critical" if status == "red" else "warning",
                        action=_ACTION,
                        publish_approved=False,
                    )
                else:
                    state = "clear"
                    SEARCH_HEALTH_ALERT_ACTIVE.labels(name).set(0)
            else:
                self._unhealthy[name] = 0
                SEARCH_HEALTH_UNHEALTHY_STREAK.labels(name).set(0)
                if was_active:
                    recovery += 1
                    self._recovery[name] = recovery
                    SEARCH_HEALTH_RECOVERY_STREAK.labels(name).set(recovery)
                    if recovery >= self.clear_after:
                        self._active.remove(name)
                        self._recovery[name] = 0
                        recovery = 0
                        state = "clear"
                        transitioned = True
                        SEARCH_HEALTH_ALERT_ACTIVE.labels(name).set(0)
                        SEARCH_HEALTH_RECOVERY_STREAK.labels(name).set(0)
                        SEARCH_HEALTH_ALERT_TRANSITIONS.labels(name, "cleared").inc()
                        self.log.info(
                            "search_health_alert_cleared",
                            cluster=name,
                            health_status=status,
                            correlation_id=current,
                            severity="info",
                            action="Continue normal search-health monitoring.",
                            publish_approved=False,
                        )
                    else:
                        state = "active"
                        SEARCH_HEALTH_ALERT_ACTIVE.labels(name).set(1)
                else:
                    self._recovery[name] = 0
                    SEARCH_HEALTH_RECOVERY_STREAK.labels(name).set(0)
                    SEARCH_HEALTH_ALERT_ACTIVE.labels(name).set(0)
                    state = "clear"

        return SearchHealthAlertSignal(
            cluster=name,
            health_status=status,
            state=state,
            transitioned=transitioned,
            correlation_id=current,
            unhealthy_streak=bad if unhealthy else 0,
            recovery_streak=recovery,
            action=_ACTION if state == "active" else "Continue normal search-health monitoring.",
            publish_approved=False,
        )


async def probe_opensearch_health(
    endpoint: str,
    *,
    timeout_seconds: float = 2.0,
    transport: httpx.AsyncBaseTransport | None = None,
) -> str:
    """Return only green/yellow/red/unreachable; never expose response bodies."""
    if not endpoint.startswith(("http://", "https://")):
        raise ValueError("endpoint must be HTTP(S)")
    try:
        async with httpx.AsyncClient(timeout=timeout_seconds, transport=transport) as client:
            response = await client.get(f"{endpoint.rstrip('/')}/_cluster/health", params={"local": "true"})
            response.raise_for_status()
            status = str(response.json().get("status", "")).lower()
            return status if status in {"green", "yellow", "red"} else "unreachable"
    except (httpx.HTTPError, ValueError, TypeError):
        return "unreachable"


search_health_alerts = SearchHealthAlertManager()
