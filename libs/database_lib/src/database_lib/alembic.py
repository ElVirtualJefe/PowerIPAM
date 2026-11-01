"""
Common Alembic Functionalities for database migrations
"""

from __future__ import annotations

from alembic import context
from alembic.script import ScriptDirectory
from alembic.migration import MigrationContext

from sqlalchemy import engine_from_config
from sqlalchemy.pool import NullPool
from sqlalchemy.engine import Connection
from sqlalchemy.schema import MetaData


def run_migrations(
        target_metadata: MetaData,
        *,
        database_url: str | None = None
        script_location: str | None = None,
        config: context.Config | None = None,
) -> None:
    """
    Run migrations for the provided model metadata.

    The calling service is responsible for passing the Alembic config
    and migration script path relevant to its schema.
    """

    cfg = config or context.config

    if database_url is not None:
        # Escape percent interpolation
        cfg.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))

    if script_location is not None:
        cfg.set_main_option("script_location", script_location)

    if context.is_offline_mode():
        _run_offline(cfg, target_metadata)
    else:
        _run_online(cfg, target_metadata)


def _run_offline(cfg: context.Config, target_metadata: MetaData) -> None:
    """Run offline migrations for the given target metadata."""

    context.configure(
        url=cfg.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()


def _run_online(cfg: context.Config, target_metadata: MetaData) -> None:
    """Run online migrations for the given target metadata."""

    connection: Connection | None = cfg.attributes.get("connection")

    if connection is not None:
        _run_with_connection(connection, target_metadata)
        return

    # Come back and update this later
    # Needs to reflect actual configuration information
    conn = engine_from_config(
        cfg.get_section(cfg.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=NullPool
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


def has_pending_migrations(
    connection: Connection,
    *,
    script_location: str | None = None
) -> bool:
    """Check if there are pending migrations for the given connection."""

    config = context.config
    if script_location is not None:
        config.set_main_option("script_location", script_location)
        
    script = ScriptDirectory.from_config(config)

    current_heads = MigrationContext.configure(connection).get_current_heads()
    start = current_heads or "base"

    return next(
        script.iterate_revisions("heads", start),
        None
    ) is not None
