"""Rate limiting middleware configuration.

This module provides rate limiting functionality using SlowAPI,
allowing configurable request limits per time period.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from aelus.core.config import Settings


def create_limiter(settings: Settings) -> Limiter | None:
    """Create and configure rate limiter.

    Creates a SlowAPI Limiter instance configured with the settings
    from the application configuration. Returns None if rate limiting
    is disabled.

    Args:
        settings: Application settings containing rate limit configuration.

    Returns:
        Configured Limiter instance, or None if rate limiting is disabled.

    Examples:
        >>> from aelus.core.config import Settings
        >>> settings = Settings(rate_limit_enabled=True, rate_limit_requests=100)
        >>> limiter = create_limiter(settings)
        >>> limiter is not None
        True
    """
    if not settings.rate_limit_enabled:
        return None

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[
            f"{settings.rate_limit_requests}/{settings.rate_limit_period}s"
        ],
        enabled=settings.rate_limit_enabled,
    )
    return limiter
