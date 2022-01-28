import os
from tempfile import TemporaryFile

from fastapi import HTTPException, status

from api.dao.file import *
from api.dao.user import *
from config import Config

from core.database.models.access_rights_enum import AccessRights

from core.schemas.file import File as FileSchema, FileInDb
from core.schemas.permission import Permission
from core.schemas.user import UserDb


async def create_file_service(file_name: str, temp_file: TemporaryFile, user: UserDb):
    contents = await temp_file.read()

    created_file = create_file_dao(FileSchema(filename=file_name), Config.STORAGE_DIR, temp_file.file.tell())

    link_user_file_dao(user, created_file, AccessRights.OWNER)
    full_file_path = os.path.join(created_file.filepath, str(created_file.id))
    new_file = open(full_file_path, "wb")
    new_file.write(contents)

    return created_file


async def get_file_by_id_service(file_id: uuid.UUID, user: UserDb) -> Union[FileInDb, None]:
    user_files = get_user_files_dao(user)
    for file in user_files:
        if file.id == file_id:
            # TODO update timestamp
            return file

    return None


async def rename_file_service(file_id: uuid.UUID, file_rename: FileSchema, user: UserDb):
    found = False
    for assoc in get_user_files_assoc_dao(user):
        if assoc.file.id == file_id:
            found = True
            # TODO access perms
            if assoc.access_rights == AccessRights.OWNER:
                rename_file_by_id_dao(assoc.file.id, file_rename.filename)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def share_file_service(file_id: uuid.UUID, current_user: UserDb, permissions: List[Permission]):
    file_schema = get_file_by_id_dao(file_id)
    assoc = get_assoc_dao(current_user, file_schema)

    if assoc.access_rights != AccessRights.OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    for permission in permissions:
        shared_user_orm = get_user_by_username_dao(permission.username)
        link_user_file_dao(shared_user_orm, file_schema, permission.permission)


async def delete_file_by_id_service(file_id: uuid.UUID, user: UserDb):
    found = False
    for assoc in get_user_files_assoc_dao(user):
        print(assoc)
        if assoc.file.id == file_id:
            found = True
            if assoc.access_rights == AccessRights.OWNER:
                filepath = os.path.join(assoc.file.filepath, str(assoc.file_id))
                delete_file_by_id_dao(file_id)
                os.remove(filepath)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
