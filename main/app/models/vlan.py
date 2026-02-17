from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression as exp
from sqlalchemy import Column,String,DateTime,SmallInteger
from sqlalchemy import func,text
import uuid
from datetime import datetime
from helpers.constants import BASE

class vLanModel(BASE):
    """
    vLAN Model
    """

    __tablename__ = "vlans"

    id = Column(UUID(True), primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String(48))
    vlanNumber = Column(SmallInteger, nullable=False)
    description = Column(String(250))
    subnets = relationship('subnetModel', backref='subnets', lazy=True)
    dateLastEdited = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    dateCreated = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f'''<
id: {self.id}
name: {self.name}
vlanNumber: {self.vlanNumber}
description: {self.description}
dateLastEdited: {self.dateLastEdited}
dateCreated: {self.dateCreated}
>'''


    def __str__(self):
        return f"<vLAN: {self.vlanNumber} - {self.name}>"