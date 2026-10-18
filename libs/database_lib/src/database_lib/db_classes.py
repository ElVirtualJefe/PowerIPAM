from .config import DatabaseSettings
from . import app_logger

from collections.abc import Generator
from uuid import UUID, uuid4
from datetime import UTC, datetime
from sqlalchemy import DateTime, func, create_engine, text, FetchedValue, Uuid, MetaData
from sqlalchemy.engine import Engine
#from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
from sqlalchemy.exc import OperationalError, IntegrityError
from contextlib import contextmanager
from . import exceptions as exc


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    """Common Base to inherit for applications"""
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

class UUIDPrimaryKeyMixin:
    """Mixin to automatically apply UUID primary keys"""
    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()")
    )

class TimestampMixin:
    """Mixin to inject standard creation and modification tracking"""
    
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=func.now()
    )

    date_last_edited: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=FetchedValue()
    )

class DatabaseManager:
    """
    Docstring for class PowerIpamDbConnection
    """

    def __init__(self,config: DatabaseSettings):
        """
        Initializes the DatabaseManager with the given database configuration.

        Args:
            config (DatabaseConfig): The database configuration object containing connection parameters and pool settings.
        """

        self.config = config

        self.engine: Engine = create_engine(
            config.connection_url,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_timeout=config.pool_timeout,
            pool_recycle=config.pool_recycle,
            pool_pre_ping=True,
            echo=config.echo,
        )

        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

        #self.Session = scoped_session(self.session_factory)

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Provides a context manager for database sessions, handling commits, rollbacks, and exceptions.
        Yields a database session and ensures proper commit, rollback, and cleanup.

        Returns:
            Generator: A database session within the context manager.
        """

        session = self.session_factory()
        try:
            yield session
            session.commit()
        except OperationalError as e:
            session.rollback()
            app_logger.error(f"Database connectivity issue: {str(e)}")
            raise exc.DatabaseConnectionError("Could not connect to the database infrastructure.") from e
        except IntegrityError as e:
            session.rollback()
            app_logger.warning(f"Database integrity violation: {str(e)}")
            raise exc.DuplicateEntryError("The data violates unique validation rules.") from e
        except Exception as e:
            session.rollback()
            app_logger.error(f"Unexpected database exception: {str(e)}")
            raise exc.DatabaseError(f"Database operation failed: {str(e)}") from e
        finally:
            session.close()

    def check_health(self) -> bool:
        """Executes a low-overhead ping to verify database liveness."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            app_logger.critical(f"Database health check failure: {str(e)}")
            return False

    def dispose(self) -> None:
        """
        Disposes of the database engine and cleans up resources.
        """
        self.engine.dispose()
