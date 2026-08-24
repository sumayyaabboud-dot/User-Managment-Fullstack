from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from app.database import get_database
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import UserRegisterSchema, UserRole

class UserService:

    @staticmethod
    async def register_user(data: UserRegisterSchema, role: UserRole = UserRole.CLIENT):
        """regist new user and add it to mongo db"""
        db = get_database()
        existing = await db.users.find_one({"email": data.email})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered"
            )
        
        user_dict = data.dict()
        user_dict["password"] = hash_password(data.password)
        user_dict["type"] = role.value
        user_dict["is_deleted"] = False
        user_dict["deleted_at"] = None
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()

        result = await db.users.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        user_dict.pop("_id", None)
        user_dict.pop("password", None)
        return user_dict

    @staticmethod
    async def authenticate_user(email: str, password: str):
        """verify from entering and creating data JWT Token"""
        db = get_database()
        user = await db.users.find_one({"email": email})

        if not user or user.get("is_deleted", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials or account is deactivated"
            )

        if not verify_password(password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": str(user["_id"]), "type": user["type"]})
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    async def get_all_users(page: int, limit: int, filters: dict):
        """ get alla users exist with filters Pagination"""
        db = get_database()
        query = {"is_deleted": False}

        if filters.get("city"):
            query["city"] = {"$regex": filters["city"], "$options": "i"}
        if filters.get("type"):
            query["type"] = filters["type"]
        if filters.get("age") is not None:
            query["age"] = filters["age"]
        if filters.get("first_name"):
            query["first_name"] = {"$regex": filters["first_name"], "$options": "i"}
        if filters.get("last_name"):
            query["last_name"] = {"$regex": filters["last_name"], "$options": "i"}
        if filters.get("email"):
            query["email"] = {"$regex": filters["email"], "$options": "i"}

        skip = (page - 1) * limit
        total_users = await db.users.count_documents(query)
        cursor = db.users.find(query).skip(skip).limit(limit)
        
        users = []
        async for user in cursor:
            user["id"] = str(user.pop("_id"))
            user.pop("password", None)

            #  translate the string date to suitable JSON
            for field in ["created_at", "updated_at", "deleted_at"]:
                if isinstance(user.get(field), datetime):
                    user[field] = user[field].isoformat()

            users.append(user)

        total_pages = (total_users + limit - 1) // limit if limit > 0 else 1

        return {
            "users": users,
            "pagination": {
                "page": page,
                "limit": limit,
                "total_users": total_users,
                "total_pages": total_pages
            }
        }

    @staticmethod
    async def get_user_by_id(user_id: str):
        """ get spacefic user by ID"""
        db = get_database()
        try:
            user = await db.users.find_one({"_id": ObjectId(user_id), "is_deleted": False})
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user["id"] = str(user.pop("_id"))
        user.pop("password", None)
        return user

    @staticmethod
    async def update_user(user_id: str, update_data: dict, is_admin: bool = False):
        """update the data user safty"""
        db = get_database()

        if not is_admin and "type" in update_data:
            update_data.pop("type", None)

        if "email" in update_data and update_data["email"]:
            try:
                existing = await db.users.find_one({"email": update_data["email"], "_id": {"$ne": ObjectId(user_id)}})
                if existing:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already taken")
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

        if "password" in update_data and update_data["password"]:
            update_data["password"] = hash_password(update_data["password"])

        filtered_data = {k: v for k, v in update_data.items() if v is not None}
        filtered_data["updated_at"] = datetime.utcnow()

        try:
            result = await db.users.find_one_and_update(
                {"_id": ObjectId(user_id), "is_deleted": False},
                {"$set": filtered_data},
                return_document=True
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        result["id"] = str(result.pop("_id"))
        result.pop("password", None)
        return result

    @staticmethod
    async def delete_user(user_id: str):
        """Soft Delete for user"""
        db = get_database()
        now = datetime.utcnow()
        try:
            result = await db.users.find_one_and_update(
                {"_id": ObjectId(user_id), "is_deleted": False},
                {"$set": {"is_deleted": True, "deleted_at": now, "updated_at": now}},
                return_document=True
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return {"message": "User deleted successfully"}

    @staticmethod
    async def create_user(data: UserRegisterSchema, role: UserRole = UserRole.CLIENT):
        """Admin creation method mapping to register_user functionality"""
        # data dictionary، Model
        if isinstance(data, dict):
            data = UserRegisterSchema(**data)
        return await UserService.register_user(data, role)