"""Unit tests for health check endpoints."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check(self, client: TestClient) -> None:
        """Test basic health endpoint."""
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Aelus"
        assert "timestamp" in data
        assert "version" in data

    def test_health_check_version(self, client: TestClient) -> None:
        """Test health endpoint returns correct version."""
        response = client.get("/health/")
        data = response.json()
        assert data["version"] == "0.1.0"

    def test_readiness_check(self, client: TestClient) -> None:
        """Test readiness endpoint."""
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["service"] == "Aelus"

    def test_liveness_check(self, client: TestClient) -> None:
        """Test liveness endpoint."""
        response = client.get("/health/live")
        assert response.status_code == 204
        assert response.content == b""

    def test_health_response_timestamp_format(self, client: TestClient) -> None:
        """Test that timestamp is in ISO format."""
        response = client.get("/health/")
        data = response.json()
        # Should be parseable as ISO datetime
        assert "T" in data["timestamp"]
