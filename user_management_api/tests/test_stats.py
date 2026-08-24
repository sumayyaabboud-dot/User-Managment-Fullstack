import pytest
from app.database import get_database

pytestmark = pytest.mark.anyio

async def test_stats_endpoints(client):
    # 1. create testing account (active , removed)
    user1 = {
        "first_name": "Active1", "last_name": "User", "email": "act1@example.com",
        "phone": "+96170123456", "city": "Tripoli", "age": 20, "password": "Password123"
    }
    user2 = {
        "first_name": "Active2", "last_name": "User", "email": "act2@example.com",
        "phone": "+96170123456", "city": "Tripoli", "age": 30, "password": "Password123"
    }
    await client.post("/auth/register", json=user1)
    await client.post("/auth/register", json=user2)

    # 2. testing for (GET /stats/count)
    res_count = await client.get("/stats/count")
    assert res_count.status_code == 200
    assert res_count.json()["total_users"] >= 2

    # 3. testing for (GET /stats/average-age)
    res_age = await client.get("/stats/average-age")
    assert res_age.status_code == 200
    assert "average_age" in res_age.json()

    # 4. testing for (GET /stats/top-cities)
    res_cities = await client.get("/stats/top-cities")
    assert res_cities.status_code == 200
    assert "cities" in res_cities.json()