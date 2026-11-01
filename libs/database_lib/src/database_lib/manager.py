"""
Database manager for handling database connections and sessions.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.orm import sessionmaker, Session

from .config import DatabaseSettings, get_database_settings
from .exceptions import DatabaseError, DatabaseConnectionError, DuplicateEntryError
from .logging_utils import get_db_logger


class DatabaseManager:
    """
    Shared database manager for SQLAlchemy-backed services.
    """

    def __init__(
        self,
        config: DatabaseSettings | None = None,
        *,
        logger_name: str = "database_lib"
    ) -> None:
        
        self._config = config or get_database_settings()
        self._logger = get_db_logger(logger_name)

        self._engine: Engine = create_engine(
            self._config.database_url,
            pool_size=self._config.pool_size,
            max_overflow=self._config.max_overflow,
            pool_timeout=self._config.pool_timeout,
            pool_recycle=self._config.pool_recycle,
            pool_pre_ping=self._config.pool_pre_ping,
            echo=self._config.echo
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False
        )

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Provide a session scope for database operations.

        Yields:
            Session: A SQLAlchemy session instance.
        """
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except OperationalError as exc:
            session.rollback()
            self._logger.exception("Operational error occurred while using the database session.")
            raise DatabaseConnectionError(
                "Could not connect to the database infrastructure."
            ) from exc
        except IntegrityError as exc:
            session.rollback()
            self._logger.warning("Integrity error occurred while using the database session", exc_info=exc)
            raise DuplicateEntryError(
                "The data violates unique validation rules."
            ) from exc
        except Exception as exc:
            session.rollback()
            self._logger.exception("Unexpected error occurred while using the database session.")
            raise DatabaseError(f"Database operation failed: {exc}") from exc
        finally:
            session.close()

    def check_health(self) -> bool:
        """
        Check the health of the database connection.

        Returns:
            bool: True if the database is reachable, False otherwise.
        """
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as exc:
            self._logger.critical("Health check failed for the database connection: %s", exc)
            return False

    def dispose(self) -> None:
        """
        Dispose of the database engine and release any resources.
        """
        self._engine.dispose()
