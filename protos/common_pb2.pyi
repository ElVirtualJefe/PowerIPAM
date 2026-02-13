from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class StateId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE: _ClassVar[StateId]
    ONLINE: _ClassVar[StateId]
    RESERVED: _ClassVar[StateId]
    UNUSED: _ClassVar[StateId]
OFFLINE: StateId
ONLINE: StateId
RESERVED: StateId
UNUSED: StateId
