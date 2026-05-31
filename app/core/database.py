"""
Database module for Jakasipul Core API.
Manages MongoDB connection using Motor (async driver).
"""

from motor.motor_asyncio import AsyncClient, AsyncDatabase
from app.core.config import settings

# Global database connection
db_client: AsyncClient = None
db: AsyncDatabase = None


async def init_db():
    """Initialize MongoDB connection using Motor."""
    global db_client, db
    
    try:
        db_client = AsyncClient(settings.mongodb_url)
        db = db_client[settings.database_name]
        
        # Verify connection
        await db_client.admin.command("ping")
        print(f"✅ Connected to MongoDB: {settings.database_name}")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def close_db():
    """Close MongoDB connection."""
    global db_client
    
    if db_client:
        db_client.close()
        print("✅ MongoDB connection closed")


async def get_db() -> AsyncDatabase:
    """Get database instance for dependency injection."""
    return db


async def get_collection(collection_name: str):
    """Get a specific collection from the database."""
    return db[collection_name]
