"""
Provides the Subnet model for the core_service application.
"""

from database_lib.db_classes import TimestampMixin, UUIDPrimaryKeyMixin, Base

from sqlalchemy import Uuid, Column, String, ForeignKey, Boolean, DateTime
from sqlalchemy import text
from sqlalchemy.orm import relationship


class SubnetModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "subnets"

    name = Column(
        String(48),
        nullable=False,
        index=True
    )
    display_name = Column(
        String(128)
    )
    description = Column(
        String(200)
    )
    ip_addresses = relationship(
        'IpAddressModel',
        backref='ip_addresses',
        lazy='True'
    )
    master_subnet_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("subnets.id"),
        nullable=True
    )
    vlan_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("vlans.id"),
        nullable=True
    )
    allow_requests = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false")
    )
    date_last_scanned = Column(
        DateTime(timezone=True),
        nullable=True
    )
    date_last_discovered = Column(
        DateTime(timezone=True),
        nullable=True
    )
    do_discovery = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false")
    )
    do_scan = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false")
    )

    def __repr__(self):
        return f"""<
id: {self.id}
name: {self.name}
display_name: {self.display_name}
description: {self.description}
master_subnet_id: {self.master_subnet_id}
allow_requests: {self.allow_requests}
do_discovery: {self.do_discovery}
do_scan: {self.do_scan}
date_last_scanned: {self.date_last_scanned}
date_last_discovered: {self.date_last_discovered}
date_created: {self.date_created}
date_last_edited: {self.date_last_edited}
>"""

    def __str__(self):
        return f"<ID: {self.id} - Subnet Name: {self.name}>"
