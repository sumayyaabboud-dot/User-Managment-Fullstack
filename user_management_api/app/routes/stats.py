from fastapi import APIRouter
from app.database import get_database

router = APIRouter( prefix="/stats", tags=["Stats"])

@router.get("/count")
async def get_user_count():
    """number of active users (except the removed account)"""
    db = get_database()
    count = await db.users.count_documents({"is_deleted": False})
    return {"total_users": count}

@router.get("/average-age")
async def get_average_age():
    """avarege of active users age"""
    db = get_database()
    pipeline = [
        {"$match": {"is_deleted": False, "age": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": None, "avg_age": {"$avg": "$age"}}}
    ]
    cursor = db.users.aggregate(pipeline)
    result = await cursor.to_list(length=1)

    if not result:
        return {"average_age": 0.0}

    avg = result[0].get("avg_age", 0.0)
    return {"average_age": round(avg, 2)}

@router.get("/top-cities")
async def get_top_cities():
    """most 3 exist cities for active users"""
    db = get_database()
    pipeline = [
        {"$match": {"is_deleted": False, "city": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$city", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 3}
    ]
    cursor = db.users.aggregate(pipeline)
    cities = []
    async for doc in cursor:
        cities.append({"city": doc["_id"], "count": doc["count"]})

    return {"cities": cities}