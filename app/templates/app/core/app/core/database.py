from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class DatabaseManager:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    def connect_to_database(self):
        """Opens a pool of asynchronous sessions to the MongoDB cluster."""
        self.client = AsyncIOMotorClient(settings.database_url)
        self.db = self.client[settings.MONGO_DB_NAME]
        print(f"🔌 Connected to MongoDB database: {settings.MONGO_DB_NAME}")

    def close_database_connection(self):
        """Gracefully closes all open database connections pool links."""
        if self.client:
            self.client.close()
            print("🛑 Closed MongoDB database connections.")

# Instantiated as a global manager across lifecycle events
db_manager = DatabaseManager()
