import logging
from . import logger,APPLICATION_NAME
app_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{logger.whoami(logging.currentframe()).split(".")[0]}')

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .db_classes import 

db_connection = PowerIpamDbConnection
engine = create_engine(

)

SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)

@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations"""
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
