from core.database.connection import DatabaseConnection
from typing import Union, List

from core.schemas.user import UserCreate as UserCreateSchema, UserDb as UserDbSchema, User as UserSchema
from core.schemas.file import FileInDb as FileInDbSchema

from core.database.models import User as UserOrm, File as FileOrm, UserFilesAssociation

Session = DatabaseConnection.get_session()
session = Session()


def create_user_dao(new_user: UserCreateSchema) -> UserDbSchema:
    # TODO user with username already exists
    new_user_db = UserOrm(**dict(new_user))
    session.add(new_user_db)
    session.commit()
    return UserDbSchema.from_orm(new_user_db)


# TODO check if correct
def get_user_by_username_dao(username: str) -> Union[UserDbSchema, None]:
    users = list(session.query(UserOrm).filter(UserOrm.username == username))
    if len(users) == 0:
        return None
    return UserDbSchema.from_orm(users[0])


def get_full_user_by_username_dao(username: str) -> Union[UserCreateSchema, None]:
    users = list(session.query(UserOrm).filter(UserOrm.username == username))
    if len(users) == 0:
        return None
    return UserCreateSchema.from_orm(users[0])


def get_user_files_dao(user: UserDbSchema) -> List[FileInDbSchema]:
    user_orm = session.get(UserOrm, user.id)
    files = []

    for assoc in user_orm.files:
        files.append(assoc.file)

    return files


def get_user_files_assoc_dao(user: UserDbSchema):
    user_orm = session.get(UserOrm, user.id)
    return list(user_orm.files)


def get_assoc_dao(user: UserDbSchema, file: FileInDbSchema):
    user_orm = session.get(UserOrm, user.id)
    file_orm = session.get(FileOrm, file.id)
    assoc = session.get(UserFilesAssociation, (user_orm.id, file_orm.id))
    session.commit()

    print(assoc)
    return assoc
