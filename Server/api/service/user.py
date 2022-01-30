from api.dao.user import create_user_dao, get_user_by_username_dao, get_user_files_dao
from core.schemas.user import UserCreate, UserDb
from core.auth.hash import get_password_hash
from core.schemas.file import FileWithPermission

from typing import Optional, List


def get_user_files_service(user: UserDb, pattern: Optional[str]) -> List[FileWithPermission]:
    return get_user_files_dao(user, pattern)


def create_user_service(new_user: UserCreate) -> UserDb:
    hashed_pw = get_password_hash(new_user.password)
    new_user.password = hashed_pw
    return create_user_dao(new_user)
