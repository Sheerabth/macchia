from core.database.connection import DatabaseConnection

from core.schemas.file import File as FileSchema, FileInDb as FileInDbSchema
from core.schemas.user import UserOut as UserOutSchema

from core.database.models import File as FileOrm, User as UserOrm, UserFilesAssociation
from core.database.models.access_rights_enum import AccessRights

Session = DatabaseConnection.get_session()
session = Session()


def create_file_dao(new_file: FileSchema, file_path) -> FileInDbSchema:
    file_orm = FileOrm(Filename=new_file.filename, Filepath=file_path)
    session.add(file_orm)
    session.commit()

    return FileInDbSchema.from_orm(file_orm)


def link_user_file(user: UserOutSchema, file: FileInDbSchema, access_rights: AccessRights):
    user_orm = session.get(UserOrm, user.id)
    file_orm = session.get(FileOrm, file.id)

    user_file_assoc = UserFilesAssociation(AccessRights=access_rights)
    user_file_assoc.file = file_orm
    user_file_assoc.user = user_orm

    user_orm.files.append(user_file_assoc)
    session.commit()

    print(user_orm)
    print(file_orm)


