from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr
from app.models.user import UserRegisterSchema, UserRole
from app.services.user_service import UserService

router = APIRouter(tags=["Authentication"])

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_client(data: UserRegisterSchema):
    """regieter for new account (Client)"""
    return await UserService.register_user(data, role= UserRole.CLIENT)

@router.post("/register/admin", status_code=status.HTTP_201_CREATED)
async def register_admin(data: UserRegisterSchema):
    """register for new account (Admin)"""
    return await UserService.register_user(data, role=UserRole.ADMIN)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: LoginSchema):
    """ log in and get the Access Token"""
    return await UserService.authenticate_user(
        email=credentials.email, 
        password=credentials.password
    )