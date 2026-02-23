from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression as exp
from sqlalchemy import Column,String,DateTime,ForeignKey,Boolean
from sqlalchemy import func,text
from datetime import datetime
from helpers.constants import BASE

class SubnetModel(BASE):
    """
    Subnet Model
    """

    # table name
    __tablename__ = 'subnets'

    id                  = Column(UUID(True), primary_key=True, server_default=text('gen_random_uuid()'))
    name                = Column(String(48), nullable=False)
    displayName         = Column(String(128))
    description         = Column(String(200))
    ipAddresses         = relationship('IpAddressModel', backref='ipAddresses', lazy=True)
    masterSubnet_id     = Column(UUID(True), ForeignKey('subnets.id'), nullable=True)
    vlan_id             = Column(UUID(True), ForeignKey('vlans.id'), nullable=True)
    allowRequests       = Column(Boolean, server_default=exp.false(), nullable=False)
    dateLastEdited      = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    dateLastScanned     = Column(DateTime(timezone=True))
    dateLastDiscovered  = Column(DateTime(timezone=True))
    dateCreated         = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    doDiscovery         = Column(Boolean, server_default=exp.false())
    doScan              = Column(Boolean, server_default=exp.false())


    def __repr__(self):
        return f'''<---
id: {self.id}
name: {self.name}
displayName: {self.displayName}
masterSubnet_id: {self.masterSubnet_id}
allowRequests: {self.allowRequests}
doDiscovery: {self.doDiscovery}
doScan: {self.doScan}
dateLastScanned: {self.dateLastScanned}
dateLastDiscovered: {self.dateLastDiscovered}
dateCreated: {self.dateCreated}
--->'''

    def __str__(self):
        return f"<Subnet Name: {self.name} - {self.id}>"

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr