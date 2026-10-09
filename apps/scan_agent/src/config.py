from functools import lru_cache

from typing import ClassVar
#from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    This class provides all of the settings for the microservice.
    """
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encodings = "utf-8",
        frozen = True,
        extra = "forbid"
    )

    # Application and service metadata
    app_name: ClassVar[str] = "PowerIPAM"
    app_ver: ClassVar[str] = "v0.0.1-alpha"
    service_name: ClassVar[str] = "scan-agent"
    service_ver: ClassVar[str] = "0.1.0.0000"

    # Application Constants
    NMAP_ARGUMENTS: ClassVar[dict] = {
        "pingScan": "-R -sP -PE -T4",
        "baseScan": "-T4 -PS21,22,80,443,3389 --open"
    }

    # Environment and logging settings
    environment: str = "development"
    log_level: str = "DEBUG"

    # Database settings
    database_url: str | None = None
    database_username: str | None = None
    database_password: str | None = None



@lru_cache
def get_settings() -> Settings:
    """
    This function loads all the Settings constants and returns them in an object.
    """

    return Settings()