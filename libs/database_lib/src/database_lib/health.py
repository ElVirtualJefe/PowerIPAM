"""
Health check utilities for the database.
"""

from .manager import DatabaseManager


def is_database_healthy(manager: DatabaseManager) -> bool:
    """
    Check if the database is healthy.

    Args:
        manager (DatabaseManager): The database manager instance.

    Returns:
        bool: True if the database is healthy, False otherwise.
    """
    try:
        return manager.check_health()
    except Exception:
        return False

def get_database_health_status(manager: DatabaseManager) -> dict:
    """
    Get the health status of the database.

    Args:
        manager (DatabaseManager): The database manager instance.

    Returns:
        dict: A dictionary containing the health status of the database.
    """
    try:
        return {"healthy": manager.check_health()}
    except Exception:
        return {"healthy": False}
