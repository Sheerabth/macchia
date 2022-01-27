from fastapi import APIRouter, Depends
from typing import List

from api.service.user import get_user_files_service
from core.schemas.user import UserDb
from core.schemas.file import File, FileInDb
from core.auth.auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserDb)
async def read_users_me(current_user: UserDb = Depends(get_current_user)):
    return current_user


@router.get("/files", response_model=List[FileInDb])
async def get_user_files(current_user: UserDb = Depends(get_current_user)):
    files = get_user_files_service(current_user)
    return files
