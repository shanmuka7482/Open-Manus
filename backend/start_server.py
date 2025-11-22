"""
Server startup script for Windows that ensures proper event loop policy
is set before uvicorn starts the FastAPI application.

This is required for Playwright to work correctly on Windows.
"""
import sys


# CRITICAL: Set the event loop policy BEFORE any other imports
if sys.platform == "win32":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import uvicorn


if __name__ == "__main__":
    # Run uvicorn with the api app
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info",
    )
