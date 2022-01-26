from core.database.connection import DatabaseConnection
from typing import Union, List

from core.schemas.user import UserCreate as UserCreateSchema, UserOut as UserOutSchema, User as UserSchema
from core.schemas.file import FileInDb as FileInDbSchema

from core.database.models import User as UserOrm

Session = DatabaseConnection.get_session()
session = Session()


def create_user_dao(new_user: UserCreateSchema) -> UserOutSchema:
    # TODO user with username already exists
    new_user_db = UserOrm(Username=new_user.username, Password=new_user.password)
    session.add(new_user_db)
    session.commit()
    return UserOutSchema.from_orm(new_user_db)


# TODO check if correct
def get_user_by_username_dao(username: str) -> Union[UserOutSchema, None]:
    users = list(session.query(UserOrm).filter(UserOrm.Username == username))
    if len(users) == 0:
        return None
    return UserOutSchema.from_orm(users[0])


def get_full_user_by_username_dao(username: str) -> Union[UserCreateSchema, None]:
    users = list(session.query(UserOrm).filter(UserOrm.Username == username))
    if len(users) == 0:
        return None
    return UserCreateSchema.from_orm(users[0])


def get_user_files_dao(user: UserOutSchema) -> List[FileInDbSchema]:
    user_orm = session.get(UserOrm, user.id)
    files = []

    for assoc in user_orm.files:
        files.append(assoc.file)

    return files
