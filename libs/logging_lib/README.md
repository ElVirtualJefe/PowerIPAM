# logging-lib

A shared Python logging library for microservice applications.

## Features

- Configurable console output for local development
- Syslog-compatible stdout logs
- JSON structured log records
- Request-scoped logging context
- Optional database sink for JSON log entries
- Works as a reusable package in other applications

## Installation

From the library directory:

```bash
pip install -e .
```

Or from another project:

```toml
[project]
dependencies = [
  "logging-lib>=0.3.0",
]
```

## Basic console usage

```python
import logging
from logging_lib import configure_logging, set_context

configure_logging(
    service_name="orders-api",
    environment="production",
    log_format="syslog",
    level="INFO",
)

set_context(request_id="req-123", user_id="42")

logging.getLogger("orders").info("Order processed")
```

## JSON logging

```python
import logging
from logging_lib import configure_logging

configure_logging(
    service_name="inventory-api",
    environment="production",
    log_format="json",
    level="INFO",
)

logging.getLogger("inventory").info("Inventory synced")
```

## Writing structured logs to a database

```python
import logging
import sqlite3

from logging_lib import configure_logging

conn = sqlite3.connect("app_logs.db")

configure_logging(
    service_name="billing-api",
    environment="production",
    log_format="syslog",
    level="INFO",
    database_connection=conn,
    database_table_name="application_logs",
)

logging.getLogger("billing").info("Invoice created")
```

The database handler creates the table automatically if it does not already exist.

## Request context

```python
from logging_lib import set_context, clear_context, get_context

set_context(request_id="abc-123", trace_id="trace-456")
print(get_context())

clear_context()
```

Context values are automatically included in structured logs and syslog fields.
