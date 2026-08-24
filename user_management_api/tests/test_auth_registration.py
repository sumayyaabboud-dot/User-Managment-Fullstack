import pytest

pytestmark = pytest.mark.anyio

# ----------------------------------------------------
# 1. test for (Successful Registration)
# ----------------------------------------------------
async def test_register_client_success(client):
    payload = {
        "first_name": "Somiya",
        "last_name": "Abboud",
        "email": "somiya@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 22,
        "password": "Password123"
    }
    response = await client.post("/auth/register", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "somiya@example.com"
    assert data.get("type") == "client" or data.get("role") == "client"
    assert "password" not in data


# ----------------------------------------------------
# 2. block the register for admin by Public Endpoint
# ----------------------------------------------------
async def test_register_public_admin_attempt_fails_or_forces_client(client):
    payload = {
        "first_name": "Hacker",
        "last_name": "User",
        "email": "hacker@example.com",
        "phone": "+96170111222",
        "city": "Beirut",
        "age": 25,
        "type": "admin",
        "password": "Password123"
    }
    response = await client.post("/auth/register", json=payload)

    if response.status_code == 201:
        assert response.json().get("type") == "client"
    else:
        assert response.status_code == 422


# ----------------------------------------------------
# 3. testin for (Duplicate Email)
# ----------------------------------------------------
async def test_register_duplicate_email(client):
    payload = {
        "first_name": "User",
        "last_name": "One",
        "email": "duplicate@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 24,
        "password": "Password123"
    }
    first_res = await client.post("/auth/register", json=payload)
    assert first_res.status_code == 201

    second_res = await client.post("/auth/register", json=payload)
    assert second_res.status_code in [400, 409]
    assert "already registered" in second_res.json()["detail"].lower() or "exists" in second_res.json()["detail"].lower()


# ----------------------------------------------------
# 4. test for (Invalid Email)
# ----------------------------------------------------
async def test_register_invalid_email(client):
    payload = {
        "first_name": "Somiya",
        "last_name": "Abboud",
        "email": "not-an-email",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 22,
        "password": "Password123"
    }
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 422


# ----------------------------------------------------
# 5. testing for (Invalid Phone)
# ----------------------------------------------------
async def test_register_invalid_phone(client):
    payload = {
        "first_name": "Somiya",
        "last_name": "Abboud",
        "email": "phone_test@example.com",
        "phone": "abc12345",
        "city": "Tripoli",
        "age": 22,
        "password": "Password123"
    }
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 422


# ----------------------------------------------------
# 6. testing for empty blank and non-logic age 
# ----------------------------------------------------
async def test_register_empty_names_and_invalid_age(client):
    payload_empty_name = {
        "first_name": "",
        "last_name": "Abboud",
        "email": "empty_name@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": 22,
        "password": "Password123"
    }
    res1 = await client.post("/auth/register", json=payload_empty_name)
    assert res1.status_code == 422

    payload_invalid_age = {
        "first_name": "Somiya",
        "last_name": "Abboud",
        "email": "invalid_age@example.com",
        "phone": "+96170123456",
        "city": "Tripoli",
        "age": -5,
        "password": "Password123"
    }
    res2 = await client.post("/auth/register", json=payload_invalid_age)
    assert res2.status_code == 422