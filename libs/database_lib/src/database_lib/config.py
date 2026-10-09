"""
Configuration to be used by the database library.
"""

from functools import lru_cache

from typing import ClassVar
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix = "DATABASE_",
        env_file = ".env",
        env_file_encodings = "utf-8",
        frozen = True,
        extra = "forbid"
    )

    lib_name: ClassVar[str] = "databse-lib"
    lib_ver: ClassVar[str] = "0.1.0.0000"

    # Environment and logging settings
    environment: str = "development"
    log_level: str = "DEBUG"

    url: str | None = Field(
        default=None,
        description="The database connection URL"
    )

    # Database connection pool settings
    pool_size: int = Field(
        default=5,
        ge=1,
        description="The maximum number of connections in the database connection pool"
    )
    max_overflow: int = Field(
        default=10,
        ge=0,
        description="The maximum number of connections to allow beyond the pool_size"
    )
    pool_timeout: int = Field(
        default=30,
        ge=0,
        description="The maximum number of seconds to wait for a connection from the pool"
    )
    pool_recycle: int = Field(
        default=1800,
        ge=0,
        description="The maximum number of seconds a connection can live before being recycled"
    )

    echo: bool = False

    # Database connection parameters
    username: str | None = None
    password: SecretStr | None = None
    host: str | None = None
    port: int | None = Field(
        default=None,
        ge=1, le=65535,
        description="The port number for the database connection"
    )
    name: str | None = None

    @property
    def connection_url(self) -> str:
        """
        Returns the connection URL for the database.
        
        If DATABASE_URL is set, it will be used. Otherwise, the URL will be constructed from the individual connection parameters.

        Returns:
            str: The connection URL for the database.
        """

        if self.url:
            return self.url
        
        if not all(
            value is not None
            for value in (
                self.username,
                self.password,
                self.host,
                self.port,
                self.name
            )
        ):
            raise ValueError(
                "All individual connection parameters (username, password, host, port, name) must be set if DATABASE_URL is not provided."
            )

        password = self.password.get_secret_value()

        return f"postgresql+psycopg2://{self.username}:{password}@{self.host}:{self.port}/{self.name}"

@lru_cache(maxsize=None)
def get_database_settings() -> DatabaseSettings:
    """
    Returns the cached database settings instance.

    Returns:
        DatabaseSettings: The database settings instance.
    """
    return DatabaseSettings()
