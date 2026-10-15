"""
Provides the IpAddress model for the core_service application.
"""

from database_lib.db_classes import TimestampMixin, UUIDPrimaryKeyMixin, Base

from sqlalchemy import Uuid, Column, String, ForeignKey, Boolean, DateTime
from sqlalchemy import text, cast


class IpAddressModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ip_addresses"

    subnet_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("subnets.id"),
        nullable=False
    )
    ip_address = Column(
        String(15),
        unique=False,
        nullable=False,
        index=True
    )
    is_gateway = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false")
    )
    is_available = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false")
    )
    description = Column(
        String(200)
    )
    hostname = Column(
        String(64)
    )
    mac_address = Column(
        String(17)
    )
    owner = Column(
        String(100)
    )
    state_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("ip_address_states.id"),
        nullable=False,
        server_default=cast("00000000-0000-0000-0000-000000000000", Uuid(as_uuid=True)),
        default=Uuid("00000000-0000-0000-0000-000000000000")
    )
    date_last_scanned = Column(
        DateTime(timezone=True),
        nullable=True
    )
    date_last_seen = Column(
        DateTime(timezone=True),
        nullable=True
    )

    def __repr__(self):
        return f'''<
id: {self.id}
ip_address: {self.ip_address}
hostname: {self.hostname}
mac_address: {self.mac_address}
description: {self.description}
owner: {self.owner}
is_gateway: {self.is_gateway}
is_available: {self.is_available}
date_last_seen: {self.date_last_seen}
date_last_scanned: {self.date_last_scanned}
date_created: {self.date_created}
date_last_edited: {self.date_last_edited}
>'''

    def __str__(self):
        return f"<{self.id} - IP={self.ip_address}>"
