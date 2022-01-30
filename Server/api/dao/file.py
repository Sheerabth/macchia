import uuid

from api.dao.user import get_assoc_dao
from core.database.connection import DatabaseConnection
import datetime

from core.schemas.file import File as FileSchema, FileInDb as FileInDbSchema
from core.schemas.user import UserDb as UserDbSchema

from core.database.models import File as FileOrm, User as UserOrm, UserFilesAssociation
from core.database.models.access_rights_enum import AccessRights

Session = DatabaseConnection.get_session()
session = Session()


def create_file_dao(new_file: FileSchema, file_path: str, file_size: int) -> FileInDbSchema:
    file_orm = FileOrm(**dict(new_file),
                       filepath=file_path,
                       file_size=file_size,
                       created_time=datetime.datetime.utcnow())
    session.add(file_orm)
    session.commit()

    return FileInDbSchema.from_orm(file_orm)


def link_user_file_dao(user: UserDbSchema, file: FileInDbSchema, access_rights: AccessRights):
    user_orm = session.get(UserOrm, user.id)
    file_orm = session.get(FileOrm, file.id)

    user_file_assoc = UserFilesAssociation(access_rights=access_rights)
    user_file_assoc.file = file_orm
    user_file_assoc.user = user_orm

    user_orm.files.append(user_file_assoc)
    session.commit()


def unlink_user_file_dao(user: UserDbSchema, file: FileInDbSchema):
    user_orm = session.get(UserOrm, user.id)
    file_orm = session.get(FileOrm, file.id)

    assoc = session.get(UserFilesAssociation, (user_orm.id, file_orm.id))
    if assoc is None:
        return

    session.delete(assoc)
    session.commit()


def rename_file_by_id_dao(file_id: uuid.UUID, new_name: str):
    file_orm = session.get(FileOrm, file_id)
    file_orm.filename = new_name
    session.commit()


def delete_file_by_id_dao(file_id: uuid.UUID):
    file_orm = session.get(FileOrm, file_id)
    for assoc in file_orm.users:
        session.delete(assoc)

    session.delete(file_orm)
    session.commit()


def get_file_by_id_dao(file_id: uuid.UUID) -> FileInDbSchema:
    file_orm = session.get(FileOrm, file_id)
    return FileInDbSchema.from_orm(file_orm)


def update_file_size_dao(file_id: uuid.UUID, size: int):
    file_orm = session.get(FileOrm, file_id)
    file_orm.file_size = size
    session.commit()


def update_permission_dao(user: UserDbSchema, file: FileInDbSchema, new_permission: AccessRights):
    assoc = get_assoc_dao(user, file)
    assoc.access_rights = new_permission
    session.commit()
