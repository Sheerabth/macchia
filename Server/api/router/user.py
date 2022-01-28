from fastapi import APIRouter, Depends
from typing import List, Optional

from api.service.user import get_user_files_service
from core.schemas.user import UserDb
from core.schemas.file import File, FileWithPermission
from core.auth.auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserDb)
async def read_users_me(current_user: UserDb = Depends(get_current_user)):
    return current_user


@router.get("/files", response_model=List[FileWithPermission])
async def get_user_files(pattern: Optional[str] = None, current_user: UserDb = Depends(get_current_user)):
    files = get_user_files_service(current_user, pattern)
    return files
