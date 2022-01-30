from api.dao.user import create_user_dao, get_user_by_username_dao, get_user_files_dao
from core.schemas.user import UserCreate, UserDb
from core.auth.hash import get_password_hash
from core.schemas.file import FileWithPermission

from typing import Optional, List

from uvicorn.config import logger


def get_user_files_service(user: UserDb, pattern: Optional[str]) -> List[FileWithPermission]:
    files = get_user_files_dao(user, pattern)
    logger.info(f"Returning files of user {user.username} matching the pattern {pattern}")
    return files


def create_user_service(new_user: UserCreate) -> UserDb:
    hashed_pw = get_password_hash(new_user.password)
    new_user.password = hashed_pw
    created_user = create_user_dao(new_user)
    logger.info(f"New user {created_user.username} added")
    return created_user
