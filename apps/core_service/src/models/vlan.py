"""
Provides the Vlan model for the core_service application.
"""

from database_lib.db_classes import TimestampMixin, UUIDPrimaryKeyMixin, Base

from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.orm import relationship


class VlanModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "vlans"

    name = Column(
        String(48),
        nullable=False,
        index=True
    )
    vlan_number = Column(
        SmallInteger,
        nullable=False,
        index=True
    )
    description = Column(
        String(200),
        nullable=True
    )
    subnets = relationship(
        'SubnetModel',
        backref='subnets',
        lazy='True'
    )

    def __repr__(self):
        return f"""<
id: {self.id}
name: {self.name}
vlan_number: {self.vlan_number}
description: {self.description}
date_last_edited: {self.date_last_edited}
date_created: {self.date_created}
>"""

    def __str__(self):
        return f"<vLAN: {self.vlan_number} - {self.name}>"
