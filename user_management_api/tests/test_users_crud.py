import pytest
from bson import ObjectId
from app.database import get_database

pytestmark = pytest.mark.anyio

# ----------------------------------------------------
# 1. testing for fetching data for user by ID (for admin)
# ----------------------------------------------------
async def test_get_user_by_id_as_admin(client):
    # create user account
    user_data = {
        "first_name": "Sumayya",
        "last_name": "Abboud",
        "email": "sumayya_get@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 22,
        "password": "Password123"
    }
    reg_res = await client.post("/auth/register", json=user_data)
    user_id = reg_res.json().get("id") or reg_res.json().get("_id")

    # convert the user in database to admin  to skip admin required
    db = get_database()
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"type": "admin"}})

    # login to get the token
    login_res = await client.post("/auth/login", json={"email": "sumayya_get@example.com", "password": "Password123"})
    token = login_res.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    
    # requist for fetch user by ID
    response = await client.get(f"/users/{user_id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "sumayya_get@example.com"
    assert data["first_name"] == "Sumayya"


# ----------------------------------------------------
# 2. testing for rejected fetching data without admin 
# ----------------------------------------------------
async def test_get_user_by_id_unauthorized_for_client(client):
    # create normal client account  
    user_data = {
        "first_name": "Normal",
        "last_name": "Client",
        "email": "client_only@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 22,
        "password": "Password123"
    }
    reg_res = await client.post("/auth/register", json=user_data)
    user_id = reg_res.json().get("id") or reg_res.json().get("_id")

    #  login as client
    login_res = await client.post("/auth/login", json={"email": "client_only@example.com", "password": "Password123"})
    token = login_res.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    
    # rejected the request and return 403 Forbidden becauce of require_admin
    response = await client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 403


# ----------------------------------------------------
# 3. testing for (PUT /users/{user_id})
# ----------------------------------------------------
async def test_update_user_as_admin(client):
    user_data = {
        "first_name": "Sumayya",
        "last_name": "Abboud",
        "email": "sumayya_update@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 22,
        "password": "Password123"
    }
    reg_res = await client.post("/auth/register", json=user_data)
    user_id = reg_res.json().get("id") or reg_res.json().get("_id")

    # give the permission for admin 
    db = get_database()
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"type": "admin"}})

    login_res = await client.post("/auth/login", json={"email": "sumayya_update@example.com", "password": "Password123"})
    token = login_res.json().get("access_token")

    update_payload = {
        "first_name": "SumayyaUpdated",
        "city": "Beirut"
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.put(f"/users/{user_id}", json=update_payload, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "SumayyaUpdated"
    assert data["city"] == "Beirut"