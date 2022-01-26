from api.dao.user import create_user_dao, get_user_by_username_dao, get_user_files_dao
from core.schemas.user import UserCreate, UserOut
from core.hash import get_password_hash


def get_user_by_username_service(username: str) -> UserOut:
    return get_user_by_username_dao(username)


def get_user_files_service(user: UserOut):
    return get_user_files_dao(user)


def create_user_service(new_user: UserCreate):
    hashed_pw = get_password_hash(new_user.password)
    new_user.password = hashed_pw
    return create_user_dao(new_user)
