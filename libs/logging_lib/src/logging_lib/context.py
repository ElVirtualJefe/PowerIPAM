from __future__ import annotations

from contextvars import ContextVar
from typing import Any
from inspect import getframeinfo

_context: ContextVar[dict[str, Any]] = ContextVar(
    "service_logging_context",
    default=[]
)

def set_context(**values: Any) -> None:
    """Add or replace values in the current execution context."""
    current = dict(_context.get())
    current.update(values)
    _context.set(current)

def remove_context(**values: Any) -> None:
    """Add or replace values in the current execution context."""
    current = dict(_context.get())
    for key in values.keys():
        current.pop(key, None)
    _context.set(current)

def get_context() -> dict[str, Any]:
    """Return a copy of the current logging context."""
    return dict(_context.get())

def clear_context() -> None:
    """Clear context for the current task or request."""
    _context.set({})

def whoami(frame:FrameType) -> str:
    """
    Docstring for whoami
    
    :param frame: Description
    :return: Description
    :rtype: Any
    """

    frame_info = getframeinfo(frame)
    #print(f'{frame=}')
    #print(f'{frame_info.__module__=}')
    #print(f'{frame_info.function=}')
    #print(f'{frame_info.filename=}')
    filename = frame_info.filename.rsplit("\\" if "\\" in __file__ else "/",maxsplit=1)[-1]
    #print(f'{filename=}')
    if frame_info.function == "<module>":
        #print("It's a file...")
        return filename
    return f'{frame_info.function}'
