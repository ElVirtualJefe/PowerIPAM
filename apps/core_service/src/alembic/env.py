from alembic import context

from database_lib.alembic import run_migrations
from database_lib.db_classes import Base

from core_service.config import get_settings
import core_service.models

settings = get_settings()

run_migrations(
    target_metadata=Base.metadata,
    database_url=settings.database_url
)
