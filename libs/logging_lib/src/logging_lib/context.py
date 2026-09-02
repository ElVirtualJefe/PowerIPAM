from __future__ import annotations

from contextvars import ContextVar
from typing import Any

_context: ContextVar[dict[str, Any]] = ContextVar(
    "service_logging_context",
    default=[]
)

def set_context(**values: Any) -> None:
    """Add or replace values in the current execution context."""
    current = dict(_context.get())
    current.update(values)
    _context.set(current)

def get_context() -> dict[str, Any]:
    """Return a copy of the current logging context."""
    return dict(_context.get())

def clear_context() -> None:
    """Clear context for the current task or request."""
    _context.set({})

