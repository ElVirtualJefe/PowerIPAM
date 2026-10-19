from __future__ import annotations

import logging
from contextvars import ContextVar
import uuid

# Optional trace ID contextvar that applications can set per-request.
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")

class TraceMicroserviceFilter(logging.Filter):
    """
    Filter that ensures each record has a trace_id attribute; if none exists
    we generate a UUID. This can be attached to a handler if the application
    wants trace_id populated automatically.
    """

    def filter(self, record: logging.LogRecord) -> bool:

        record.trace_id = trace_id_var.get() or str(uuid.uuid4())
        return True
