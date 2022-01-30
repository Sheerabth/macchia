from api.service.user import create_user_service
from core.schemas.token import Token
from core.schemas.user import UserCreate, UserDb
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends

from api.service.auth import login_service

from config import Config

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    token = await login_service(form_data)
    return token


@router.post("/register", response_model=UserDb)
async def register_user(user: UserCreate):
    return create_user_service(user)
