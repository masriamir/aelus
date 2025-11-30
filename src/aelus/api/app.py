"""FastAPI application factory.

This module provides the main application factory for creating and configuring
the FastAPI application with all necessary middleware, routes, and settings.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from aelus.api.middleware.rate_limit import create_limiter
from aelus.api.routes.health import router as health_router
from aelus.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Application lifespan manager.

    Handles startup and shutdown events for the FastAPI application.

    Args:
        app: The FastAPI application instance.

    Yields:
        None during application runtime.
    """
    # Startup
    logger.info("Starting Aelus API...")
    yield
    # Shutdown
    logger.info("Shutting down Aelus API...")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure FastAPI application.

    Factory function that creates a fully configured FastAPI application
    with CORS, rate limiting, and all routes registered.

    Args:
        settings: Application settings. If None, loads from environment.

    Returns:
        Configured FastAPI application instance.

    Examples:
        >>> app = create_app()
        >>> app.title
        'Aelus'
    """
    if settings is None:
        settings = get_settings()

    openapi_tags: list[dict[str, Any]] = [
        {
            "name": "health",
            "description": "Health check endpoints for monitoring service status",
        },
        {
            "name": "projects",
            "description": "Ableton Live project operations",
        },
    ]

    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        openapi_url=settings.openapi_url,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        lifespan=lifespan,
        openapi_tags=openapi_tags,
    )

    # Store settings in app state
    app.state.settings = settings

    # Add CORS middleware
    if settings.cors_enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add rate limiting
    if settings.rate_limit_enabled:
        limiter = create_limiter(settings)
        if limiter is not None:
            app.state.limiter = limiter
            app.add_exception_handler(
                RateLimitExceeded,
                _rate_limit_exceeded_handler,  # type: ignore[arg-type]
            )
            app.add_middleware(SlowAPIMiddleware)

    # Include routers
    app.include_router(health_router, prefix="/health", tags=["health"])

    return app


# Default app instance for uvicorn
app = create_app()
