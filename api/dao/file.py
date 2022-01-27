from core.database.connection import DatabaseConnection
import datetime

from core.schemas.file import File as FileSchema, FileInDb as FileInDbSchema
from core.schemas.user import UserDb as UserOutSchema

from core.database.models import File as FileOrm, User as UserOrm, UserFilesAssociation
from core.database.models.access_rights_enum import AccessRights

Session = DatabaseConnection.get_session()
session = Session()


def create_file_dao(new_file: FileSchema, file_path: str, file_size: int) -> FileInDbSchema:
    file_orm = FileOrm(**dict(new_file), filepath=file_path, file_size=file_size, created_time=datetime.datetime.now())
    session.add(file_orm)
    session.commit()

    return FileInDbSchema.from_orm(file_orm)


def link_user_file_dao(user: UserOutSchema, file: FileInDbSchema, access_rights: AccessRights):
    user_orm = session.get(UserOrm, user.id)
    file_orm = session.get(FileOrm, file.id)

    user_file_assoc = UserFilesAssociation(access_rights=access_rights)
    user_file_assoc.file = file_orm
    user_file_assoc.user = user_orm

    user_orm.files.append(user_file_assoc)
    session.commit()

    print(user_orm)
    print(file_orm)


# def get_file_by_id_dao(file: )
# TODO
# def update_file_access_time(file: FileInDbSchema, time: )