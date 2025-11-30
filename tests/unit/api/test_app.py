"""Unit tests for FastAPI application setup."""

import pytest
from fastapi.testclient import TestClient

from aelus.api.app import create_app
from aelus.core.config import Settings


@pytest.mark.unit
class TestApp:
    """Test FastAPI application setup."""

    def test_app_creation(self, test_app) -> None:  # type: ignore[no-untyped-def]
        """Test app creates successfully."""
        assert test_app.title == "Aelus"
        assert test_app.version == "0.1.0"

    def test_openapi_schema(self, client: TestClient) -> None:
        """Test OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "Aelus"

    def test_docs_available(self, client: TestClient) -> None:
        """Test documentation endpoints are available."""
        response = client.get("/docs")
        assert response.status_code == 200

        response = client.get("/redoc")
        assert response.status_code == 200

    def test_app_settings_in_state(self, test_app, test_settings) -> None:  # type: ignore[no-untyped-def]
        """Test that settings are stored in app state."""
        assert hasattr(test_app.state, "settings")
        assert test_app.state.settings.debug is True

    def test_app_with_rate_limiting_enabled(self) -> None:
        """Test that rate limiter is attached when enabled."""
        settings = Settings(rate_limit_enabled=True)
        app = create_app(settings)
        assert hasattr(app.state, "limiter")

    def test_app_without_rate_limiting(self, test_app_no_rate_limit) -> None:  # type: ignore[no-untyped-def]
        """Test that rate limiter is not attached when disabled."""
        assert not hasattr(test_app_no_rate_limit.state, "limiter")
