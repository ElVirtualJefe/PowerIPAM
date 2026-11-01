
"""
Database Manager Library

Exposes the Public Interface for the shared database infrastructure package.
"""

from .alembic import has_pending_migrations, run_migrations
from .base import Base
from .config import DatabaseSettings, get_database_settings
from .exceptions import DatabaseConnectionError, DatabaseError, DuplicateEntryError
from .manager import DatabaseManager
from .mixins import TimestampMixin, UUIDPrimaryKeyMixin

__all__ = [
    "DatabaseSettings",
    "get_database_settings",
    "Base",
    "DatabaseManager",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    "DatabaseError",
    "DatabaseConnectionError",
    "DuplicateEntryError",
    "run_migrations",
    "has_pending_migrations",
]
