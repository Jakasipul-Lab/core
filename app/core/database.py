"""
Database module for Jakasipul Core API.
Manages MongoDB connection using Motor (async driver).
"""

from motor.motor_asyncio import AsyncClient, AsyncDatabase
from app.core.config import settings
from fastapi import HTTPException

# Global database connection references
db_client: AsyncClient = None
db: AsyncDatabase = None


async def init_db():
    """Initialize MongoDB connection using Motor."""
    global db_client, db
    
    try:
        # Added serverSelectionTimeoutMS to prevent hanging if MongoDB is down
        db_client = AsyncClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000
        )
        
        # Fixed naming property to match our Pydantic settings config
        db = db_client[settings.mongo_db_name]
        
        # Verify connection immediately via administrative ping
        await db_client.admin.command("ping")
        print(f"✅ Connected to MongoDB database: {settings.mongo_db_name}")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        # Ensure objects stay clean if initialization fails
        db_client = None
        db = None
        raise e


async def close_db():
    """Close MongoDB connection."""
    global db_client, db
    
    if db_client:
        db_client.close()
        db_client = None
        db = None
        print("✅ MongoDB connection pool closed cleanly")


async def get_db() -> AsyncDatabase:
    """Get database instance for dependency injection."""
    if db is None:
        raise HTTPException(
            status_code=500, 
            detail="Database connection is currently unavailable."
        )
    return db


async def get_collection(collection_name: str):
    """Get a specific collection from the database."""
    current_db = await get_db()
    return current_db[collection_name]
