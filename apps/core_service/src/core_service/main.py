from logging import currentframe
from logging_lib import configure_logging, set_context, remove_context, get_logger, whoami

from config import get_settings
from pathlib import Path

from alembic import command
from alembic.config import Config


settings = get_settings()

configure_logging(
    service_name=f'[{settings.service_name} {settings.service_ver}]',
    environment=settings.environment,
    log_format="syslog",
    level=settings.log_level,
    version=settings.app_ver
)


app_logger = get_logger(settings.service_name)
app_logger.debug("---+++  Initialized Logger for %s  +++---", (__name__))

app_logger.debug('Starting Core Service Process...')

def migrate_database() -> None:
    """
    This function runs the database migrations for the core service.
    """

    db_migration_logger = get_logger(settings.service_name).getChild(f'{whoami(currentframe())}')

    alembic_ini = Path(__file__).resolve().parent.parent / "alembic.ini"
    db_migration_logger.debug("Running database migrations using alembic.ini file: %s", alembic_ini)

    alembic_cfg = Config(str(alembic_ini))
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        settings.database.connection_url.replace("%", "%%")
    )
    db_migration_logger.debug("Database URL: %s", settings.database.connection_url)
    db_migration_logger.debug("Starting database migrations...")
    command.upgrade(alembic_cfg, "head")

def serve() -> None:
    """
    This function starts the core service server.
    """

    server_logger = get_logger(settings.service_name).getChild(f'{whoami(currentframe())}')
    server_logger.info("Starting core service server...")

    migrate_database()


if __name__ == "__main__":
    """
    This is the main entry point for the core service application.
    """
    serve()
