from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String
from sqlalchemy import text
if __name__ == 'app.models.addressState':
    from app.helpers.constants import BASE
else:
    from helpers.constants import BASE

class AddressStateModel(BASE):
    """
    Address State Model
    """

    __tablename__ = "addressStates"

    id = Column(UUID(True), primary_key=True, server_default=text('gen_random_uuid()'))
    state = Column(String(48), unique=True, nullable=False)

    def __repr__(self):
        return f"<State: {self.state}>"
