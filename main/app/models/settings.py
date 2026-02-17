from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String,DateTime
from sqlalchemy import func,text
from datetime import datetime
from helpers.constants import BASE

class settingsModel(BASE):
    """
    Settings Model
    """

    __tablename__ = "settings"

    id = Column(UUID(True), primary_key=True, server_default=text('gen_random_uuid()'))
    category = Column(String(24))
    name = Column(String(48))
    value = Column(String(120))
    dateLastEdited = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    dateCreated = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Setting - {self.name}: {self.value}>"