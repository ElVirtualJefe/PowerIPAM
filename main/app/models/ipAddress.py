

from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String,ForeignKey,Boolean,DateTime
from sqlalchemy import func,text,cast
from helpers.database import Base

class IpAddressModel(Base):
    """
    IP Address Model
    """

    # table name
    __tablename__ = 'ipAddresses'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    subnet_id = Column(UUID(as_uuid=True), ForeignKey('subnets.id'), nullable=False)
    ipAddress = Column(String(15), unique=True, index=True, nullable=False)
    is_gateway = Column(Boolean, default=False, nullable=False)
    is_available = Column(Boolean, default=False, nullable=False)
    description = Column(String(200))
    hostname = Column(String(64))
    macAddress = Column(String(17))
    owner = Column(String(40))
    state_id = Column(UUID(as_uuid=True), 
        ForeignKey('addressStates.id'), 
        nullable=False, 
        server_default=cast('5a3be258-876b-4fb3-9788-61acced67be1', UUID)
    )
    dateLastSeen = Column(DateTime(timezone=True))
    dateLastEdited = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    dateCreated = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f'''<
id: {self.id}
ipAddress: {self.ipAddress}
hostname: {self.hostname}
macAddress: {self.macAddress}
description: {self.description}
owner: {self.owner}
is_gateway: {self.is_gateway}
is_available: {self.is_available}
dateLastSeen: {self.dateLastSeen}
dateCreated: {self.dateCreated}
>'''


    def __str__(self):
        return f"<id {self.id} - IP {self.ipAddress}>"