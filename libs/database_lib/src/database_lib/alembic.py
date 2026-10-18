"""
Common Alembic Functionalities
"""

from alembic import context
from alembic.script import ScriptDirectory
from alembic.migration import MigrationContext

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.schema import MetaData


def run_migrations(
        target_metadata: MetaData,
        *,
        database_url: str | None = None
) -> None:
    """Run migrations for the given target metadata."""

    config = context.config

    if database_url is not None:
        # Escape percent interpolation
        config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))

    if context.is_offline_mode():
        _run_offline(target_metadata)
    else:
        _run_online(target_metadata)


def _run_offline(target_metadata: MetaData) -> None:
    """Run offline migrations for the given target metadata."""

    context.configure(
        url=context.config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()


def _run_online(target_metadata: MetaData) -> None:
    """Run online migrations for the given target metadata."""

    connection: Connection | None = context.config.attributes.get("connection")

    if connection is not None:
        _run_with_connection(connection, target_metadata)
        return

    # Come back and update this later
    # Needs to reflect actual configuration information
    conn = engine_from_config(
        context.config.get_section(context.config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    try:
        with conn.connect() as connection:
            _run_with_connection(connection, target_metadata)
    finally:
        conn.dispose()


def _run_with_connection(
        connection: Connection,
        target_metadata: MetaData
) -> None:
    """Run migrations with the given connection and target metadata."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        transaction_per_migration=True
    )

    with context.begin_transaction():
        context.run_migrations()


def has_pending_migrations(connection: Connection) -> bool:
    """Check if there are pending migrations for the given connection."""

    config = context.config
    script = ScriptDirectory.from_config(config)

    current_heads = MigrationContext.configure(connection).get_current_heads()
    start = current_heads or "base"

    return next(
        script.iterate_revisions("heads", start),
        None
    ) is not None
