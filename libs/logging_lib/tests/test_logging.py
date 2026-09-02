import json
import logging

import pytest

from logging_lib import (
    clear_context,
    configure_logging,
    get_context,
    set_context,
)


@pytest.fixture(autouse=True)
def reset_logging():
    """
    Reset context and root logging before and after every test.

    This prevents one test's handlers or request data from affecting
    another test.
    """
    clear_context()
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers[:]
    original_level = root_logger.level

    yield

    clear_context()
    root_logger.handlers.clear()
    root_logger.handlers.extend(original_handlers)
    root_logger.setLevel(original_level)


def test_context_values_are_stored():
    set_context(
        request_id="req-123",
        service="orders-api",
    )

    context = get_context()

    assert context["request_id"] == "req-123"
    assert context["service"] == "orders-api"


def test_context_values_can_be_cleared():
    set_context(request_id="req-123")

    clear_context()

    assert get_context() == {}


def test_syslog_message_is_written_to_stdout(capsys):
    configure_logging(
        service_name="orders-api",
        environment="development",
        log_format="syslog",
        level="INFO",
    )

    set_context(request_id="req-123")

    logger = logging.getLogger("orders")
    logger.info("Order processed")

    captured = capsys.readouterr()
    output = captured.out.strip()

    assert output.startswith("<")
    assert "1 " in output
    assert "orders-api" in output
    assert "orders" in output
    assert "request_id=\"req-123\"" in output
    assert "Order processed" in output


def test_syslog_info_priority_is_correct(capsys):
    configure_logging(
        service_name="orders-api",
        log_format="syslog",
        level="INFO",
    )

    logging.getLogger("orders").info("Informational message")

    output = capsys.readouterr().out

    # Facility local0 = 16, INFO severity = 6:
    # 16 * 8 + 6 = 134
    assert output.startswith("<134>1 ")


def test_json_logging_is_valid_json(capsys):
    configure_logging(
        service_name="orders-api",
        environment="test",
        version="1.0.0",
        log_format="json",
        level="INFO",
    )

    set_context(request_id="req-456")

    logger = logging.getLogger("orders")
    logger.info(
        "Payment completed",
        extra={"payment_id": "pay-789"},
    )

    output = capsys.readouterr().out
    record = json.loads(output)

    assert record["message"] == "Payment completed"
    assert record["level"] == "INFO"
    assert record["service"] == "orders-api"
    assert record["environment"] == "test"
    assert record["version"] == "1.0.0"
    assert record["request_id"] == "req-456"
    assert record["payment_id"] == "pay-789"


def test_debug_messages_are_filtered_at_info_level(capsys):
    configure_logging(
        service_name="orders-api",
        log_format="syslog",
        level="INFO",
    )

    logging.getLogger("orders").debug("Debug message")

    output = capsys.readouterr().out

    assert output == ""


def test_error_contains_exception_details(capsys):
    configure_logging(
        service_name="orders-api",
        log_format="syslog",
        level="ERROR",
    )

    logger = logging.getLogger("orders")

    try:
        raise ValueError("Invalid order")
    except ValueError:
        logger.exception("Order processing failed")

    output = capsys.readouterr().out

    assert "Order processing failed" in output
    assert "ValueError" in output
    assert "Invalid order" in output
