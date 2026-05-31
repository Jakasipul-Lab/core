"""
Jakasipul Core: FastAPI Application Bootstrap Entry Point
Main application module for East African mobility routing and booking engine.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

# Import core modules
from app.core.config import settings
from app.core.database import init_db, close_db


# Lifespan context manager for app startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    # Startup
    print("🚀 Starting Jakasipul Core API...")
    await init_db()
    print("✅ Database connection established")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Jakasipul Core API...")
    await close_db()
    print("✅ Database connection closed")


# Initialize FastAPI application
app = FastAPI(
    title="Jakasipul Core API",
    description="East African Mobility Routing & Booking Engine",
    version="1.0.0",
    lifespan=lifespan
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "service": "Jakasipul Core API",
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - returns API info."""
    return {
        "message": "Welcome to Jakasipul Core API",
        "docs": "/docs",
        "health": "/health"
    }


# Mount static files if they exist
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Include routers (can be added later)
# from app.api import routes
# app.include_router(routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",  # Change to "main:app" if this file is NOT inside an "app" folder
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
