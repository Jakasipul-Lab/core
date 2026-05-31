"""
Jakasipul Core: FastAPI Application Bootstrap Entry Point
Main application module for East African mobility routing and booking engine.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

# Import core modules
from app.core.config import settings
from app.core.database import init_db, close_db


# Lifespan context manager for app startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    # Startup
    print(f"🚀 Starting {settings.project_name} in {settings.environment} mode...")
    await init_db()
    
    yield
    
    # Shutdown
    print(f"🛑 Shutting down {settings.project_name}...")
    await close_db()


# Initialize FastAPI application using your dynamic Pydantic settings
app = FastAPI(
    title=settings.project_name,
    description="East African Mobility Routing & Booking Engine",
    version=settings.app_version,
    lifespan=lifespan
)


# Health check endpoint (Used by your Docker healthcheck!)
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "service": settings.project_name,
        "version": settings.app_version,
        "environment": settings.environment
    }


# Root endpoint - Serves your beautiful custom HTML landing page
@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - Returns the custom HTML dashboard."""
    html_path = "app/static/index.html"
    
    # Check if the HTML dashboard exists, otherwise serve a basic fallback
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as file:
            return file.read()
            
    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>🚌 {settings.project_name}</h1>
            <p>API is running, but index.html was not found in app/static/</p>
            <a href="/docs">View API Docs</a>
        </body>
    </html>
    """


# Mount static assets if the folder exists (for CSS/JS/Images later)
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Include routers (can be uncommented as you build them out)
# from app.api import routes
# app.include_router(routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",  # Assumes running from project root folder
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )
