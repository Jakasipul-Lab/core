from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.core.database import db_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application lifecycle startup and shutdown events seamlessly,
    guaranteeing non-blocking connections to the database cluster.
    """
    # Startup: Initialize the async MongoDB connection pool
    db_manager.connect_to_database()
    yield
    # Shutdown: Clean up connections gracefully
    db_manager.close_database_connection()

# Initialize the core FastAPI instance with lifecycle management hooks
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# Bind the server HTML template directory mapping
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    """
    Serves the primary, high-performance transit routing analytics interface
    from the application root domain level.
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "project_name": settings.PROJECT_NAME}
    )

@app.get("/api/v1/health")
async def health_check():
    """
    Exposes a lightweight microservices readiness monitor to verify framework,
    environment lifecycle execution status, and database latency markers.
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected" if db_manager.client is not None else "disconnected"
    }
