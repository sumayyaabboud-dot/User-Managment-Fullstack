import sys
import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import get_database, connect_to_mongo, close_mongo_connection

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", autouse=True)
async def initialize_db_connection():
    """Ensure the database connection remains active and secure for the duration of the test suite"""
    await connect_to_mongo()
    yield
    await close_mongo_connection()

@pytest.fixture
async def client():
    """Asynclient to deliver the request"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def cleanup_database():
    """clean up database before and after testing"""
    db = get_database()
    await db.users.delete_many({})
    yield
    await db.users.delete_many({})