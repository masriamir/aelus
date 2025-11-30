"""Integration tests for API flow."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestAPIFlow:
    """Test complete API workflows."""

    def test_full_health_check_flow(self, client: TestClient) -> None:
        """Test all health endpoints in sequence."""
        # Check liveness first
        response = client.get("/health/live")
        assert response.status_code == 204

        # Check readiness
        response = client.get("/health/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"

        # Check main health
        response = client.get("/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_docs_and_schema_integration(self, client: TestClient) -> None:
        """Test documentation and schema integration."""
        # Get OpenAPI schema
        schema_response = client.get("/openapi.json")
        assert schema_response.status_code == 200

        # Verify schema structure
        schema = schema_response.json()
        assert "paths" in schema
        assert "/health/" in schema["paths"]

        # Check docs render with schema
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200

    def test_redoc_documentation(self, client: TestClient) -> None:
        """Test ReDoc documentation endpoint."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_tags(self, client: TestClient) -> None:
        """Test OpenAPI tags are properly defined."""
        response = client.get("/openapi.json")
        schema = response.json()

        tag_names = [tag["name"] for tag in schema.get("tags", [])]
        assert "health" in tag_names
