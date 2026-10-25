from __future__ import annotations

import logging
from contextvars import ContextVar
from typing import Optional
import uuid

# Optional trace ID contextvar that applications can set per-request.
trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)

class TraceMicroserviceFilter(logging.Filter):
    """
    Filter that ensures each record has a trace_id attribute; if none exists
    we generate a UUID. This can be attached to a handler if the application
    wants trace_id populated automatically.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        trace = trace_id_var.get()

        if trace:
            record.trace_id = trace
        else:
            record.trace_id = getattr(record, "trace_id", None) or str(uuid.uuid4())
        return True
