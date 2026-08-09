from __future__ import annotations

import re
from dataclasses import dataclass
from threading import Lock

from prometheus_client import Counter, Gauge

from dtmo.logging import correlation_id, get_logger, resolve_correlation_id

API_REQUEST_RESULTS = Counter(
    "dtmo_api_request_results_total",
    "Observed API request outcomes used by the bounded API error alert",
    ["route", "result"],
)
API_ERROR_STREAK = Gauge(
    "dtmo_api_error_streak",
    "Consecutive HTTP 5xx responses observed for an API route template",
    ["route"],
)
API_ERROR_RECOVERY_STREAK = Gauge(
    "dtmo_api_error_recovery_streak",
    "Consecutive non-5xx responses observed while an API error alert is active",
    ["route"],
)
API_ERROR_ALERT_ACTIVE = Gauge(
    "dtmo_api_error_alert_active",
    "Whether the bounded API error alert is active for a route template",
    ["route"],
)
API_ERROR_ALERT_TRANSITIONS = Counter(
    "dtmo_api_error_alert_transitions_total",
    "API error alert state transitions",
    ["route", "transition"],
)

_API_ACTION = (
    "Inspect the correlated request trace, recent deploys and downstream dependency health; "
    "do not retry destructive operations until the failure mode is understood."
)
_ROUTE_TEMPLATE = re.compile(r"^(?:<unmatched>|/[A-Za-z0-9_./{}:-]{0,127})$")


def _current_correlation(value: str | None) -> str:
    current = value or correlation_id.get()
    return resolve_correlation_id(None) if current == "-" else current


@dataclass(frozen=True, slots=True)
class ApiErrorAlertSignal:
    route: str
    state: str
    transitioned: bool
    correlation_id: str
    status_code: int
    consecutive_errors: int
    consecutive_recoveries: int
    raise_after: int
    clear_after: int
    action: str
    publish_approved: bool = False


class ApiErrorAlertManager:
    """Observe bounded HTTP outcomes and emit non-publishing API error alert evidence.

    Only route templates and status codes enter this observer. Raw URLs, query strings,
    request/response bodies, headers and identities are deliberately outside its input
    contract. Three consecutive 5xx outcomes raise by default; an active alert clears only
    after two consecutive non-5xx outcomes. This small hysteresis avoids single-request
    flapping while preserving rapid controlled-failure evidence.
    """

    def __init__(self, *, raise_after: int = 3, clear_after: int = 2) -> None:
        if raise_after < 1:
            raise ValueError("raise_after must be at least one")
        if clear_after < 1:
            raise ValueError("clear_after must be at least one")
        self.raise_after = raise_after
        self.clear_after = clear_after
        self._error_streak: dict[str, int] = {}
        self._recovery_streak: dict[str, int] = {}
        self._active: set[str] = set()
        self._lock = Lock()
        self.log = get_logger("api.alerts")

    def observe(
        self,
        route: str,
        *,
        status_code: int,
        correlation: str | None = None,
    ) -> ApiErrorAlertSignal:
        route_template = route.strip()
        if not _ROUTE_TEMPLATE.fullmatch(route_template):
            raise ValueError("route must be a bounded route template without request data")
        if status_code < 100 or status_code > 599:
            raise ValueError("status_code must be a valid HTTP status code")

        current_correlation = _current_correlation(correlation)
        server_error = status_code >= 500
        result = "server_error" if server_error else "non_server_error"
        API_REQUEST_RESULTS.labels(route_template, result).inc()

        with self._lock:
            was_active = route_template in self._active
            error_streak = self._error_streak.get(route_template, 0)
            recovery_streak = self._recovery_streak.get(route_template, 0)
            transitioned = False

            if server_error:
                error_streak += 1
                recovery_streak = 0
                self._error_streak[route_template] = error_streak
                self._recovery_streak[route_template] = recovery_streak
                API_ERROR_STREAK.labels(route_template).set(error_streak)
                API_ERROR_RECOVERY_STREAK.labels(route_template).set(0)

                if was_active or error_streak >= self.raise_after:
                    self._active.add(route_template)
                    state = "active"
                    API_ERROR_ALERT_ACTIVE.labels(route_template).set(1)
                    if not was_active:
                        transitioned = True
                        API_ERROR_ALERT_TRANSITIONS.labels(route_template, "raised").inc()
                        event = "api_error_alert_raised"
                    else:
                        event = "api_error_alert_active"
                    self.log.warning(
                        event,
                        route=route_template,
                        correlation_id=current_correlation,
                        severity="warning",
                        status_code=status_code,
                        consecutive_errors=error_streak,
                        raise_after=self.raise_after,
                        clear_after=self.clear_after,
                        action=_API_ACTION,
                        publish_approved=False,
                    )
                else:
                    state = "clear"
                    API_ERROR_ALERT_ACTIVE.labels(route_template).set(0)
            else:
                error_streak = 0
                self._error_streak[route_template] = 0
                API_ERROR_STREAK.labels(route_template).set(0)

                if was_active:
                    recovery_streak += 1
                    self._recovery_streak[route_template] = recovery_streak
                    API_ERROR_RECOVERY_STREAK.labels(route_template).set(recovery_streak)
                    if recovery_streak >= self.clear_after:
                        self._active.remove(route_template)
                        self._recovery_streak[route_template] = 0
                        recovery_streak = 0
                        state = "clear"
                        transitioned = True
                        API_ERROR_ALERT_ACTIVE.labels(route_template).set(0)
                        API_ERROR_RECOVERY_STREAK.labels(route_template).set(0)
                        API_ERROR_ALERT_TRANSITIONS.labels(route_template, "cleared").inc()
                        self.log.info(
                            "api_error_alert_cleared",
                            route=route_template,
                            correlation_id=current_correlation,
                            severity="info",
                            status_code=status_code,
                            clear_after=self.clear_after,
                            action="Continue normal API monitoring.",
                            publish_approved=False,
                        )
                    else:
                        state = "active"
                        API_ERROR_ALERT_ACTIVE.labels(route_template).set(1)
                        self.log.info(
                            "api_error_alert_recovering",
                            route=route_template,
                            correlation_id=current_correlation,
                            severity="info",
                            status_code=status_code,
                            consecutive_recoveries=recovery_streak,
                            clear_after=self.clear_after,
                            action="Confirm recovery with another successful request.",
                            publish_approved=False,
                        )
                else:
                    recovery_streak = 0
                    self._recovery_streak[route_template] = 0
                    API_ERROR_RECOVERY_STREAK.labels(route_template).set(0)
                    API_ERROR_ALERT_ACTIVE.labels(route_template).set(0)
                    state = "clear"

        return ApiErrorAlertSignal(
            route=route_template,
            state=state,
            transitioned=transitioned,
            correlation_id=current_correlation,
            status_code=status_code,
            consecutive_errors=error_streak,
            consecutive_recoveries=recovery_streak,
            raise_after=self.raise_after,
            clear_after=self.clear_after,
            action=_API_ACTION if state == "active" else "Continue normal API monitoring.",
            publish_approved=False,
        )


api_error_alerts = ApiErrorAlertManager()
