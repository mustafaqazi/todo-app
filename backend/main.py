"""FastAPI application entry point"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from db import create_tables, close_db
from routes import tasks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.

    Startup:
    - Creates all database tables defined in SQLModel
    - Logs initialization

    Shutdown:
    - Closes database connections
    - Logs cleanup
    """
    # Startup
    logger.info("Starting FastAPI application")
    await create_tables()
    logger.info("Database tables created/verified")

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application")
    await close_db()
    logger.info("Database connections closed")


# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(tasks.router, prefix="/api")


# Health check endpoint
@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Health check",
    description="Check if the API is running"
)
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok", "version": settings.VERSION}


# Catch-all error handler for 404
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 Not Found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Endpoint not found"}
    )


# Catch-all error handler for 405
@app.exception_handler(405)
async def method_not_allowed_handler(request, exc):
    """Handle 405 Method Not Allowed errors."""
    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content={"detail": "Method not allowed"}
    )


# Root endpoint
@app.get(
    "/",
    tags=["root"],
    summary="API Information",
    description="Get API information"
)
async def root():
    """Root endpoint with API information."""
    return {
        "title": settings.TITLE,
        "description": settings.DESCRIPTION,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
