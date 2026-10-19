from __future__ import annotations

from contextvars import ContextVar
from typing import Any
from types import FrameType
from inspect import getframeinfo

_context: ContextVar[dict[str, Any]] = ContextVar(
    "service_logging_context",
    default={}
)

def set_context(**values: Any) -> None:
    """Add or replace values in the current execution context."""
    current = dict(_context.get() or {})
    current.update(values)
    _context.set(current)

def remove_context(**values: Any) -> None:
    """Add or replace values in the current execution context."""
    current = dict(_context.get() or {})
    for key in values.keys():
        current.pop(key, None)
    _context.set(current)

def get_context() -> dict[str, Any]:
    """Return a copy of the current logging context."""
    return dict(_context.get() or {})

def clear_context() -> None:
    """Clear context for the current task or request."""
    _context.set({})

def whoami(frame:FrameType) -> str:
    """
    Return a short identifier for the current frame. This helper is intentionally
    small and dependency-free so it can be used by consumers who want a simple
    textual identifier for the current module/function.

    :param frame: frame object as returned by inspect.currentframe()
    :return: a string like 'module.py' for top-level modules or 'function_name'
    """

    frame_info = getframeinfo(frame)
    # Choose the filename portion only; preserve behavior across OSes.
    filename = frame_info.filename.rsplit("\\" if "\\" in __file__ else "/",maxsplit=1)[-1]

    if frame_info.function == "<module>":
        return filename
    return f'{frame_info.function}'
