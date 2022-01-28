from core.database.connection import DatabaseConnection
from typing import Union, List, Optional

from core.schemas.user import UserCreate as UserCreateSchema, UserDb as UserDbSchema, User as UserSchema
from core.schemas.file import FileWithPermission as FileWithPermissionSchema, FileInDb as FileInDbSchema

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


def get_user_files_dao(user: UserDbSchema, search_pattern: Optional[str]) -> List[FileWithPermissionSchema]:
    assoc_files = get_user_files_assoc_dao(user)
    print("SP: ", search_pattern)
    result = []
    for assoc in assoc_files:
        if not search_pattern:
            result.append(FileWithPermissionSchema(permission=assoc.access_rights, **assoc.file.__dict__))
        else:
            if search_pattern in assoc.file.filename:
                result.append(FileWithPermissionSchema(permission=assoc.access_rights, **assoc.file.__dict__))

    print(result)
    return result


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
