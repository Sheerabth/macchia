import sqlalchemy.exc

from core.database.connection import DatabaseConnection
from typing import Union, List, Optional

from core.schemas.user import UserCreate as UserCreateSchema, UserDb as UserDbSchema, User as UserSchema
from core.schemas.file import FileWithPermission as FileWithPermissionSchema, FileInDb as FileInDbSchema

from core.database.models import User as UserOrm, File as FileOrm, UserFilesAssociation
from core.exceptions import BadRequestException

Session = DatabaseConnection.get_session()
session = Session()


def create_user_dao(new_user: UserCreateSchema) -> UserDbSchema:
    new_user_db = UserOrm(**dict(new_user))

    try:
        session.add(new_user_db)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise BadRequestException(message="The username already exists")

    return UserDbSchema.from_orm(new_user_db)


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


def get_user_files_dao(user: UserDbSchema, search_pattern: Optional[str] = None) -> List[FileWithPermissionSchema]:
    assoc_files = get_user_files_assoc_dao(user)
    result = []
    for assoc in assoc_files:
        if not search_pattern:
            result.append(FileWithPermissionSchema(permission=assoc.access_rights, **assoc.file.__dict__))
        else:
            if search_pattern in assoc.file.filename:
                result.append(FileWithPermissionSchema(permission=assoc.access_rights, **assoc.file.__dict__))

    return result


def get_user_files_assoc_dao(user: UserDbSchema) -> List[UserFilesAssociation]:
    user_orm = session.get(UserOrm, user.id)
    return list(user_orm.files)


def get_assoc_dao(user: UserDbSchema, file: FileInDbSchema) -> Union[UserFilesAssociation, None]:
    user_orm = session.get(UserOrm, user.id)
    file_orm = session.get(FileOrm, file.id)
    assoc = session.get(UserFilesAssociation, (user_orm.id, file_orm.id))
    session.commit()

    return assoc
