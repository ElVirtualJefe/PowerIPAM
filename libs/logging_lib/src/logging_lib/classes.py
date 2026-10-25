from __future__ import annotations

import json
import logging
import os
import traceback
from datetime import datetime, timezone
from typing import Any

from .context import get_context


_RESERVED_LOG_RECORD_KEYS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


class JsonMicroserviceFormatter(logging.Formatter):
    """Format log records as one JSON object per line."""

    def __init__(
        self,
        service_name: str,
        environment: str,
        version: str | None = None,
    ) -> None:
        super().__init__()
        self.service_name = service_name
        self.environment = environment
        self.version = version

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
            "environment": self.environment,
        }

        if self.version:
            payload["version"] = self.version

        payload.update(get_context())

        for key, value in record.__dict__.items():
            if key not in _RESERVED_LOG_RECORD_KEYS and not key.startswith("_"):
                payload.setdefault(key, value)

        if record.exc_info:
            payload["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        return json.dumps(payload, default=str)


class ConsoleFormatter(logging.Formatter):
    """Readable formatter for local development."""

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        context = get_context()

        if context:
            context_text = " ".join(f"{key}={value}" for key, value in context.items())
            return f"{message} [{context_text}]"

        return message


class SyslogConsoleFormatter(logging.Formatter):
    """
    Format records as RFC 5424-like syslog messages for stdout.

    This does not open a network socket. The container runtime receives
    the formatted messages from stdout.
    """

    SEVERITY = {
        logging.DEBUG: 7,
        logging.INFO: 6,
        logging.WARNING: 4,
        logging.ERROR: 3,
        logging.CRITICAL: 2,
    }

    def __init__(
        self,
        *,
        service_name: str,
        facility: int = 16,
        hostname: str = "-",
    ) -> None:
        super().__init__()
        self.service_name = service_name
        self.facility = facility
        self.hostname = hostname

    def format(self, record: logging.LogRecord) -> str:
        severity = self.SEVERITY.get(record.levelno, 3)
        priority = self.facility * 8 + severity

        timestamp = datetime.fromtimestamp(
            record.created,
            tz=timezone.utc,
        ).isoformat(timespec="milliseconds").replace("+00:00", "Z")

        process_id = os.getpid()
        message = record.getMessage()
        structured_data = self._structured_data()

        output = (
            f"<{priority}>1 "
            f"{timestamp} "
            f"{self.hostname} "
            f"{self.service_name} "
            f"{process_id} "
            f"{record.name} "
            f"- "
            f"{structured_data} "
            f"{message}"
        )

        if record.exc_info:
            output += f"\n{self.formatException(record.exc_info)}"

        return output

    def _structured_data(self) -> str:
        context = get_context()

        if not context:
            return "-"

        fields = []

        for key, value in context.items():
            safe_key = self._sanitize_name(str(key))
            safe_value = self._escape_value(str(value))
            fields.append(f'{safe_key}="{safe_value}"')

        return "[context " + " ".join(fields) + "]"

    @staticmethod
    def _sanitize_name(value: str) -> str:
        return "".join(
            character
            for character in value
            if character.isalnum() or character in "_-"
        ) or "field"

    @staticmethod
    def _escape_value(value: str) -> str:
        return (
            value.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("]", "\\]")
            .replace("\n", "\\n")
        )


class JsonDatabaseLogHandler(logging.Handler):
    """Write structured JSON log records to a database-agnostic connection."""

    def __init__(
        self,
        *,
        connection: Any,
        table_name: str = "application_logs",
        service_name: str = "unknown-service",
        environment: str = "development",
        version: str | None = None,
        database_dialect: str | None = None,
    ) -> None:
        super().__init__()
        self.connection = self._normalize_connection(connection)
        self.table_name = self._validate_table_name(table_name)
        self.service_name = service_name
        self.environment = environment
        self.version = version
        self.database_dialect = (database_dialect or self._detect_database_dialect(self.connection)).lower()
        self._sqlalchemy_mode = self._is_sqlalchemy_connection(self.connection)
        self._ensure_table()

    @staticmethod
    def _normalize_connection(connection: Any) -> Any:
        if hasattr(connection, "connect") and not hasattr(connection, "execute"):
            try:
                return connection.connect()
            except Exception:
                return connection
        return connection

    @staticmethod
    def _validate_table_name(table_name: str) -> str:
        if not table_name or not table_name.replace("_", "").isalnum():
            raise ValueError("table_name must be a simple alphanumeric identifier")
        return table_name

    @staticmethod
    def _detect_database_dialect(connection: Any) -> str:
        dialect = getattr(connection, "dialect", None)
        if dialect is not None:
            name = getattr(dialect, "name", None)
            if name:
                return str(name)

        engine = getattr(connection, "engine", None)
        if engine is not None:
            dialect = getattr(engine, "dialect", None)
            if dialect is not None:
                name = getattr(dialect, "name", None)
                if name:
                    return str(name)

        module_name = "".join(
            (
                getattr(type(connection), "__module__", ""),
                getattr(type(connection), "__name__", ""),
            )
        ).lower()

        if "sqlite" in module_name:
            return "sqlite"
        if "postgres" in module_name or "psycopg" in module_name:
            return "postgresql"
        if "mysql" in module_name or "mariadb" in module_name:
            return "mysql"

        return "sqlite"

    @staticmethod
    def _is_sqlalchemy_connection(connection: Any) -> bool:
        return hasattr(connection, "dialect") and hasattr(connection, "execute")

    @staticmethod
    def _parameter_placeholder(database_dialect: str) -> str:
        dialect = database_dialect.lower()
        if dialect in {"postgresql", "postgres", "mysql", "mariadb", "mssql"}:
            return "%s"
        return "?"

    def _ensure_table(self) -> None:
        if self._sqlalchemy_mode:
            try:
                from sqlalchemy import text
            except ImportError:
                return

            statement = text(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "timestamp TEXT NOT NULL, "
                "level TEXT NOT NULL, "
                "logger TEXT NOT NULL, "
                "message TEXT NOT NULL, "
                "service TEXT, "
                "environment TEXT, "
                "version TEXT, "
                "payload TEXT NOT NULL"
                ")"
            )
            try:
                self.connection.execute(statement)
                self.connection.commit()
            except Exception:
                pass
            return

        create_sql = (
            f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "timestamp TEXT NOT NULL, "
            "level TEXT NOT NULL, "
            "logger TEXT NOT NULL, "
            "message TEXT NOT NULL, "
            "service TEXT, "
            "environment TEXT, "
            "version TEXT, "
            "payload TEXT NOT NULL"
            ")"
        )

        try:
            self.connection.execute(create_sql)
            try:
                self.connection.commit()
            except Exception:
                pass
        except Exception:
            pass

    def emit(self, record: logging.LogRecord) -> None:
        payload = self._payload_for_record(record)
        payload_text = json.dumps(payload, default=str)

        if self._sqlalchemy_mode:
            self._emit_sqlalchemy(record, payload, payload_text)
            return

        self._emit_dbapi(record, payload, payload_text)

    def _emit_dbapi(self, record: logging.LogRecord, payload: dict[str, Any], payload_text: str) -> None:
        placeholder = self._parameter_placeholder(self.database_dialect)
        insert_sql = (
            f"INSERT INTO {self.table_name} ("
            "timestamp, level, logger, message, service, environment, version, payload) "
            f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, "
            f"{placeholder}, {placeholder}, {placeholder}, {placeholder})"
        )
        values = (
            payload["timestamp"],
            payload["level"],
            payload["logger"],
            payload["message"],
            payload["service"],
            payload["environment"],
            payload.get("version"),
            payload_text,
        )

        try:
            self.connection.execute(insert_sql, values)
            try:
                self.connection.commit()
            except Exception:
                pass
        except Exception:
            self.handleError(record)

    def _emit_sqlalchemy(self, record: logging.LogRecord, payload: dict[str, Any], payload_text: str) -> None:
        try:
            from sqlalchemy import text
        except ImportError:
            self.handleError(record)
            return

        statement = text(
            f"INSERT INTO {self.table_name} ("
            "timestamp, level, logger, message, service, environment, version, payload) "
            "VALUES (:timestamp, :level, :logger, :message, :service, :environment, "
            ":version, :payload)"
        )
        params = {
            "timestamp": payload["timestamp"],
            "level": payload["level"],
            "logger": payload["logger"],
            "message": payload["message"],
            "service": payload["service"],
            "environment": payload["environment"],
            "version": payload.get("version"),
            "payload": payload_text,
        }

        try:
            self.connection.execute(statement, params)
            try:
                self.connection.commit()
            except Exception:
                pass
        except Exception:
            self.handleError(record)

    def _payload_for_record(self, record: logging.LogRecord) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
            "environment": self.environment,
        }

        if self.version:
            payload["version"] = self.version

        payload.update(get_context())

        for key, value in record.__dict__.items():
            if key not in _RESERVED_LOG_RECORD_KEYS and not key.startswith("_"):
                payload.setdefault(key, value)

        if record.exc_info:
            payload["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        return payload
