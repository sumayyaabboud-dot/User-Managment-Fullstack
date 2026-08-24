from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

# function ti open the connection with server
async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URL)
    print("Connected to MongoDB successfully!")

# function to close the connection with server
async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection.")

# function to have an object DB
def get_database():
    return db.client[settings.DATABASE_NAME]