import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IpAddress(_message.Message):
    __slots__ = ("id", "ip_address", "owner", "description", "is_gateway", "hostname", "state_id", "last_seen", "last_modified", "date_created", "subnet_id", "mac_address")
    ID_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_GATEWAY_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    STATE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    DATE_CREATED_FIELD_NUMBER: _ClassVar[int]
    SUBNET_ID_FIELD_NUMBER: _ClassVar[int]
    MAC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    id: str
    ip_address: str
    owner: str
    description: str
    is_gateway: bool
    hostname: str
    state_id: _common_pb2.StateId
    last_seen: _timestamp_pb2.Timestamp
    last_modified: _timestamp_pb2.Timestamp
    date_created: _timestamp_pb2.Timestamp
    subnet_id: str
    mac_address: str
    def __init__(self, id: _Optional[str] = ..., ip_address: _Optional[str] = ..., owner: _Optional[str] = ..., description: _Optional[str] = ..., is_gateway: bool = ..., hostname: _Optional[str] = ..., state_id: _Optional[_Union[_common_pb2.StateId, str]] = ..., last_seen: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_modified: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., date_created: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., subnet_id: _Optional[str] = ..., mac_address: _Optional[str] = ...) -> None: ...

class IpAddressRequest(_message.Message):
    __slots__ = ("id", "name", "subnet_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SUBNET_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    subnet_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., subnet_id: _Optional[str] = ...) -> None: ...

class IpAddressResponse(_message.Message):
    __slots__ = ("ip_address",)
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ip_address: _containers.RepeatedCompositeFieldContainer[IpAddress]
    def __init__(self, ip_address: _Optional[_Iterable[_Union[IpAddress, _Mapping]]] = ...) -> None: ...
