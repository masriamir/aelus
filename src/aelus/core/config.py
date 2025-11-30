"""Application settings configuration.

This module provides centralized configuration management using Pydantic settings,
loading values from environment variables with sensible defaults.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Settings can be configured via environment variables or a .env file.
    Environment variable names are case-insensitive.

    Attributes:
        app_name: Display name of the application.
        app_version: Current version of the application.
        app_description: Description shown in OpenAPI docs.
        host: Server bind host address.
        port: Server bind port number.
        debug: Enable debug mode for detailed logging.
        reload: Enable auto-reload for development.
        api_v1_prefix: Prefix for versioned API routes.
        openapi_url: Path to OpenAPI schema JSON.
        docs_url: Path to Swagger UI documentation.
        redoc_url: Path to ReDoc documentation.
        rate_limit_enabled: Enable or disable rate limiting.
        rate_limit_requests: Maximum requests allowed per period.
        rate_limit_period: Time period for rate limiting in seconds.
        cors_enabled: Enable or disable CORS middleware.
        cors_origins: List of allowed CORS origins.
    """

    app_name: str = "Aelus"
    app_version: str = "0.1.0"
    app_description: str = "Web-based dashboard for Ableton Live projects"

    # Server settings
    host: str = "0.0.0.0"  # noqa: S104
    port: int = 8000
    debug: bool = False
    reload: bool = False

    # API settings
    api_v1_prefix: str = "/api/v1"
    openapi_url: str = "/openapi.json"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds

    # CORS settings
    cors_enabled: bool = True
    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns a cached singleton instance of the Settings class,
    ensuring configuration is loaded only once.

    Returns:
        Settings: Application settings loaded from environment.

    Examples:
        >>> settings = get_settings()
        >>> settings.app_name
        'Aelus'
    """
    return Settings()
