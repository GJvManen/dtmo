from __future__ import annotations

import logging
import re
import sys
from contextvars import ContextVar
from typing import cast
from uuid import uuid4

import structlog

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="-")
_CORRELATION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=level.upper())
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper(), logging.INFO)
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def resolve_correlation_id(value: str | None) -> str:
    if value is not None and _CORRELATION_ID.fullmatch(value):
        return value
    return str(uuid4())


def bind_request_context(
    request_id: str,
    method: str,
    *,
    trace_id: str | None = None,
    span_id: str | None = None,
) -> None:
    fields: dict[str, str] = {"correlation_id": request_id, "method": method}
    if trace_id is not None:
        fields["trace_id"] = trace_id
    if span_id is not None:
        fields["span_id"] = span_id
    structlog.contextvars.bind_contextvars(**fields)


def clear_request_context() -> None:
    structlog.contextvars.clear_contextvars()


def get_logger(name: str = "dtmo") -> structlog.stdlib.BoundLogger:
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(name))
