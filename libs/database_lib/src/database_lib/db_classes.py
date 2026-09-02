from logging import getLogger,currentframe
from . import log_manager,APPLICATION_NAME
app_logger = getLogger(f'{APPLICATION_NAME}').getChild(f'{log_manager.whoami(currentframe()).split(".")[0]}')
app_logger.debug('Loading db_classes...')

import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, func, create_engine, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError, IntegrityError
from contextlib import contextmanager
from . import exceptions as exc



class Base(DeclarativeBase):
    """Common Base to inherit for applications"""
    pass

class UUIDPrimaryKeyMixin:
    """Mixin to automatically apply UUID primary keys"""
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

class TimestampMixin:
    """Mixin to inject standard creation and modification tracking"""
    dateCreated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    dateLastEdited: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

class DatabaseManager:
    """
    Docstring for class PowerIpamDbConnection
    """

    def __init__(self,database_url:str,pool_size:int=10,max_overflow:int=5):
        """
        Docustring for function __init__
        """

        self.engine = create_engine(
            database_url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
            connect_args={"connect_timeout":5}
        )

        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    @contextmanager
    def session_scope(self):
        """
        Docstring for function session_scope
        """

        session = self.Session()
        try:
            yield session
            session.commit()
        except OperationalError as e:
            session.rollback()
            app_logger.error(f"Database connectivity issue: {str(e)}")
            raise exc.DatabaseConnectionError("Could not connect to the database infrastructure.")
        except IntegrityError as e:
            session.rollback()
            app_logger.warn(f"Database integrity violation: {str(e)}")
            raise exc.DuplicateEntryError("The data violates unique validation rules.")
        except Exception as e:
            session.rollback()
            app_logger.error(f"Unexpected database exception: {str(e)}")
            raise exc.DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            self.Session.remove()

    def check_health(self) -> bool:
        """Executes a low-overhead ping to verify database liveness."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            app_logger.critical(f"Database health check failure: {str(e)}")
            return False   
