from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from app.models.user import UserRole
from app.core.dependencies import require_admin, get_current_user
from app.services.user_service import UserService

router = APIRouter( tags=["Users"])

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    city: Optional[str] = None,
    type: Optional[UserRole] = None,
    age: Optional[int] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    _: dict = Depends(require_admin)
):
    """show all active users"""
    filters = {
        "city": city,
        "type": type.value if type is not None else None,
        "age": age,
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }
    return await UserService.get_all_users(page, limit, filters)

# ----------------------------------------------------
# (1 Post /users) by Admin
# ----------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_by_admin(
    user_data: dict,
    _: dict = Depends(require_admin)
):
    """(for admin) create client or admin"""
    return await UserService.create_user(user_data)

# ----------------------------------------------------
# 2. routes for user profile(/users/me)
# ----------------------------------------------------
@router.get("/me", status_code=status.HTTP_200_OK)
async def get_my_profile(
    current_user: dict = Depends(get_current_user)
):
    """get data for the allow user"""
    current_user.pop("password", None)
    if "_id" in current_user:
        current_user["id"] = str(current_user.pop("_id"))
    return current_user

@router.put("/me", status_code=status.HTTP_200_OK)
async def update_my_profile(
    update_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """update the profile data (with preventing expired)"""
    # prevent for the normal user from raise himself (Admin)
    if "type" in update_data:
        update_data.pop("type")
        
    user_id = str(current_user["_id"]) if "_id" in current_user else current_user["id"]
    return await UserService.update_user(user_id, update_data, is_admin=False)

# ----------------------------------------------------
# 
# ----------------------------------------------------
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: str,
    _: dict = Depends(require_admin)
):
    """ get data for specific user by ID"""
    return await UserService.get_user_by_id(user_id)

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    update_data: dict,
    _: dict = Depends(require_admin)
):
    """(for admin) updating for data user (specefic)"""
    return await UserService.update_user(user_id, update_data, is_admin=True)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: str,
    _: dict = Depends(require_admin)
):
    """soft delete for specefic user """
    return await UserService.delete_user(user_id)