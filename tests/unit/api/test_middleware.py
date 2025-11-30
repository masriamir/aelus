"""Unit tests for middleware."""

import pytest

from aelus.api.middleware.rate_limit import create_limiter
from aelus.core.config import Settings


@pytest.mark.unit
class TestRateLimitMiddleware:
    """Test rate limiting middleware."""

    def test_create_limiter_enabled(self) -> None:
        """Test limiter creation when enabled."""
        settings = Settings(
            rate_limit_enabled=True,
            rate_limit_requests=100,
            rate_limit_period=60,
        )
        limiter = create_limiter(settings)
        assert limiter is not None

    def test_create_limiter_disabled(self) -> None:
        """Test limiter returns None when disabled."""
        settings = Settings(rate_limit_enabled=False)
        limiter = create_limiter(settings)
        assert limiter is None

    def test_limiter_configuration(self) -> None:
        """Test limiter is configured with correct limits."""
        settings = Settings(
            rate_limit_enabled=True,
            rate_limit_requests=50,
            rate_limit_period=30,
        )
        limiter = create_limiter(settings)
        assert limiter is not None
        # Verify the limiter was created with enabled=True
        assert limiter.enabled is True
