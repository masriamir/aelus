"""Health check API endpoints.

This module provides health check endpoints for monitoring service status,
including basic health checks and Kubernetes-compatible readiness/liveness probes.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Request, Response
from pydantic import BaseModel, Field

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model.

    Attributes:
        status: Current service status (healthy, ready, etc.).
        timestamp: UTC timestamp of the health check.
        version: Application version string.
        service: Service name identifier.
    """

    status: str = Field(..., description="Current service status")
    timestamp: datetime = Field(..., description="UTC timestamp of the health check")
    version: str = Field(..., description="Application version")
    service: str = Field(..., description="Service name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "timestamp": "2024-11-27T10:00:00Z",
                "version": "0.1.0",
                "service": "Aelus",
            }
        }
    }


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Basic health check",
    description="Returns current health status of the service",
)
async def health_check(request: Request) -> HealthResponse:
    """Basic health check endpoint.

    Returns the current health status of the service along with
    version information and timestamp.

    Args:
        request: The incoming HTTP request.

    Returns:
        HealthResponse with current service status.
    """
    settings = request.app.state.settings
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(UTC),
        version=settings.app_version,
        service=settings.app_name,
    )


@router.get(
    "/ready",
    response_model=HealthResponse,
    summary="Readiness check",
    description="Kubernetes-compatible readiness probe",
)
async def readiness_check(request: Request) -> HealthResponse:
    """Readiness check for Kubernetes.

    Checks if the service is ready to accept requests. This endpoint
    can be extended to verify database connections and other dependencies.

    Args:
        request: The incoming HTTP request.

    Returns:
        HealthResponse indicating readiness status.
    """
    settings = request.app.state.settings
    return HealthResponse(
        status="ready",
        timestamp=datetime.now(UTC),
        version=settings.app_version,
        service=settings.app_name,
    )


@router.get(
    "/live",
    status_code=204,
    summary="Liveness check",
    description="Kubernetes-compatible liveness probe",
)
async def liveness_check() -> Response:
    """Liveness check for Kubernetes.

    Simple endpoint that returns 204 No Content if the service is alive.
    Used by container orchestrators to detect unresponsive services.

    Returns:
        Empty response with 204 status code.
    """
    return Response(status_code=204)
