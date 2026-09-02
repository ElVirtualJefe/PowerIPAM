class DatabaseError(Exception):
    """Base exception for all database operations."""
    pass

class DatabaseConnectionError(DatabaseError):
    """Raised when the database cannot be reached."""
    pass

class DuplicateEntryError(DatabaseError):
    """Raised when a unique constraint or primary key violation occurs."""
    pass
