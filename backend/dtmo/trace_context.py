from __future__ import annotations

import re
import secrets
from contextvars import ContextVar, Token
from dataclasses import dataclass

from prometheus_client import Counter

trace_id: ContextVar[str] = ContextVar("trace_id", default="-")
span_id: ContextVar[str] = ContextVar("span_id", default="-")
trace_flags: ContextVar[str] = ContextVar("trace_flags", default="00")

TRACE_CONTEXTS = Counter(
    "dtmo_trace_context_total",
    "Inbound W3C trace-context decisions",
    ["decision"],
)

_TRACEPARENT_V00 = re.compile(
    r"^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$"
)
_ZERO_TRACE_ID = "0" * 32
_ZERO_SPAN_ID = "0" * 16


@dataclass(frozen=True, slots=True)
class TraceBinding:
    trace_token: Token[str]
    span_token: Token[str]
    flags_token: Token[str]
    trace_id: str
    span_id: str
    trace_flags: str
    incoming_accepted: bool


def parse_traceparent(value: str | None) -> tuple[str, str, str] | None:
    """Parse the bounded W3C version-00 traceparent form.

    Unknown versions, uppercase/non-hex data, all-zero identifiers, oversized values and
    extension fields are rejected. The caller then starts a fresh local trace rather than
    retaining untrusted opaque input.
    """

    if value is None or len(value) != 55:
        return None
    match = _TRACEPARENT_V00.fullmatch(value)
    if match is None:
        return None
    incoming_trace_id, parent_id, flags = match.groups()
    if incoming_trace_id == _ZERO_TRACE_ID or parent_id == _ZERO_SPAN_ID:
        return None
    return incoming_trace_id, parent_id, flags


def _new_trace_id() -> str:
    value = secrets.token_hex(16)
    while value == _ZERO_TRACE_ID:
        value = secrets.token_hex(16)
    return value


def _new_span_id() -> str:
    value = secrets.token_hex(8)
    while value == _ZERO_SPAN_ID:
        value = secrets.token_hex(8)
    return value


def begin_trace(incoming_traceparent: str | None) -> TraceBinding:
    parsed = parse_traceparent(incoming_traceparent)
    if parsed is None:
        current_trace_id = _new_trace_id()
        flags = "00"
        TRACE_CONTEXTS.labels("generated" if incoming_traceparent is None else "rejected").inc()
        accepted = False
    else:
        current_trace_id, _remote_parent_id, flags = parsed
        TRACE_CONTEXTS.labels("accepted").inc()
        accepted = True

    current_span_id = _new_span_id()
    trace_token = trace_id.set(current_trace_id)
    span_token = span_id.set(current_span_id)
    flags_token = trace_flags.set(flags)
    return TraceBinding(
        trace_token=trace_token,
        span_token=span_token,
        flags_token=flags_token,
        trace_id=current_trace_id,
        span_id=current_span_id,
        trace_flags=flags,
        incoming_accepted=accepted,
    )


def end_trace(binding: TraceBinding) -> None:
    trace_flags.reset(binding.flags_token)
    span_id.reset(binding.span_token)
    trace_id.reset(binding.trace_token)


def current_trace_id() -> str | None:
    value = trace_id.get()
    return None if value == "-" else value


def current_span_id() -> str | None:
    value = span_id.get()
    return None if value == "-" else value


def outbound_traceparent() -> str:
    """Return a bounded child traceparent for an outbound HTTP dependency call.

    If no inbound/local request trace is bound (for example a scheduled connector run), a
    fresh trace root is generated for that dependency call. No tracestate is accepted or
    propagated by this bounded baseline.
    """

    parent_trace_id = current_trace_id() or _new_trace_id()
    child_span_id = _new_span_id()
    flags = trace_flags.get() if current_trace_id() is not None else "00"
    return f"00-{parent_trace_id}-{child_span_id}-{flags}"
