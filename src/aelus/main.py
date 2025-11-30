"""Main entry point for running Aelus API server.

This module provides the command-line entry point for starting the
Aelus API server using uvicorn.
"""

import uvicorn

from aelus.api.app import create_app
from aelus.core.config import get_settings


def main() -> None:
    """Run the Aelus API application using uvicorn.

    Creates the FastAPI application with current settings and starts
    the uvicorn server with configured host, port, and logging.
    """
    settings = get_settings()
    app = create_app(settings)

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level="debug" if settings.debug else "info",
    )


if __name__ == "__main__":
    main()
