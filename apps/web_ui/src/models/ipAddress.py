

from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String,ForeignKey,Boolean,DateTime
from sqlalchemy import func,text,cast
if __name__ == 'app.models.ipAddress':
    from app.helpers.constants import BASE
else:
    from helpers.constants import BASE

class IpAddressModel(BASE):
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
        nullable=False
    )
    dateLastSeen = Column(DateTime(timezone=True))
    dateLastEdited = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    dateCreated = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f'''<
id: {self.id}
ipAddress: {self.ipAddress}
subnet_id: {self.subnet_id}
hostname: {self.hostname}
macAddress: {self.macAddress}
description: {self.description}
owner: {self.owner}
state_id: {self.state_id}
is_gateway: {self.is_gateway}
is_available: {self.is_available}
dateLastSeen: {self.dateLastSeen}
dateCreated: {self.dateCreated}
>'''


    def __str__(self):
        return f"<id: {self.id} - IP: {self.ipAddress} - is_available: {self.is_available}>"

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr
