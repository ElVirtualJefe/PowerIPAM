from __future__ import annotations

from contextvars import ContextVar
from inspect import getframeinfo
from types import FrameType
from typing import Any

_context: ContextVar[dict[str, Any]] = ContextVar(
    "service_logging_context",
    default={},
)


def set_context(**values: Any) -> None:
    """Add or replace values in the current execution context."""
    current = dict(_context.get() or {})
    current.update(values)
    _context.set(current)


def remove_context(**values: Any) -> None:
    """Remove values from the current execution context."""
    current = dict(_context.get() or {})
    for key in values:
        current.pop(key, None)
    _context.set(current)


def get_context() -> dict[str, Any]:
    """Return a snapshot of the current logging context."""
    return dict(_context.get() or {})


def clear_context() -> None:
    """Clear the logging context for the current task or request."""
    _context.set({})


def whoami(frame: FrameType) -> str:
    """
    Return a short identifier for the current frame.

    Example:
        module.py
        function_name
    """
    frame_info = getframeinfo(frame)
    filename = frame_info.filename.rsplit("\\" if "\\" in __file__ else "/", maxsplit=1)[-1]

    if frame_info.function == "<module>":
        return filename
    return frame_info.function
