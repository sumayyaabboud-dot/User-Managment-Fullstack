import pytest

pytestmark = pytest.mark.anyio

# ----------------------------------------------------
# 1. test for successful login
# ----------------------------------------------------
async def test_login_success(client):
    # create user
    user_data = {
        "first_name": "Somiya",
        "last_name": "Abboud",
        "email": "login_test@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 22,
        "password": "Password123"
    }
    await client.post("/auth/register", json=user_data)

    # register entery (use email instead of username، واستخدام json=)
    login_payload = {
        "email": "login_test@example.com",  # correction here 
        "password": "Password123"
    }
    response = await client.post("/auth/login", json=login_payload) #   using json=
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


# ----------------------------------------------------
# 2  test for login by incorrect password
# ----------------------------------------------------
async def test_login_invalid_password(client):
    user_data = {
        "first_name": "Somiya",
        "last_name": "Abboud",
        "email": "wrong_pass@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 22,
        "password": "CorrectPassword123"
    }
    await client.post("/auth/register", json=user_data)

    login_payload = {
        "email": "wrong_pass@example.com", # correction here
        "password": "WrongPassword123"
    }
    response = await client.post("/auth/login", json=login_payload) # using json=
    
    assert response.status_code == 401


# ----------------------------------------------------
# 3. test for blocking removed account
# ----------------------------------------------------
async def test_soft_deleted_user_cannot_login(client):
    user_data = {
        "first_name": "Deleted",
        "last_name": "User",
        "email": "deleted@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 30,
        "password": "Password123"
    }
    reg_res = await client.post("/auth/register", json=user_data)
    #  ID according to storage(id أو _id)
    user_id = reg_res.json().get("id") or reg_res.json().get("_id")

    from app.database import get_database
    from bson import ObjectId
    db = get_database()
    # immplementing for softe delete manualy
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"is_deleted": True}})

    login_payload = {
        "email": "deleted@example.com", # correction here 
        "password": "Password123"
    }
    response = await client.post("/auth/login", json=login_payload)
    
    # the rejecteg done acordin to (how you code 401,403)
    assert response.status_code in [400, 401, 403]