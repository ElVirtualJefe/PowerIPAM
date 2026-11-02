# database-lib

Shared SQLAlchemy database infrastructure for microservices.

This package provides a reusable database foundation for applications that need:

- PostgreSQL-first configuration support
- SQLAlchemy engine/session management
- shared metadata and model mixins
- lightweight database health checks
- Alembic migration helper utilities
- service-aware logging integration

The library is intentionally infrastructure-focused. It does not own service-specific models or migration scripts. Each service should define its own model classes and Alembic migration structure.

## Features

- DatabaseSettings with environment-based configuration
- DatabaseManager with pooled engine and session lifecycle
- Base declarative metadata for shared model usage
- TimestampMixin and UUIDPrimaryKeyMixin
- DB health checks
- Alembic migration utility helpers
- Optional integration with logging-lib
- Test-friendly design using ephemeral PostgreSQL containers

## Installation

Install the package from your local workspace or package index:

```bash
pip install database-lib