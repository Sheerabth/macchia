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

from core.exceptions import NotFoundException, ForbiddenException

import shutil


async def create_file_service(file_name: str, temp_file: TemporaryFile, user: UserDb):
    created_file = create_file_dao(FileSchema(filename=file_name), Config.STORAGE_DIR, -1)
    link_user_file_dao(user, created_file, AccessRights.OWNER)

    full_file_path = os.path.join(Config.STORAGE_DIR, str(created_file.id))
    shutil.copyfileobj(temp_file.file, open(full_file_path, "wb"))

    file_size = os.path.getsize(full_file_path)
    update_file_size_dao(created_file.id, file_size)

    return get_file_by_id_dao(created_file.id)


async def get_file_by_id_service(file_id: uuid.UUID, user: UserDb) -> Union[FileInDb, None]:
    user_files = get_user_files_dao(user)
    print(user_files)
    for file in user_files:
        if file.id == file_id:
            return file

    return None


async def update_file_service(file_id: uuid.UUID, temp_file: TemporaryFile, current_user: UserDb):
    file_to_update = get_file_by_id_dao(file_id)

    assoc = get_assoc_dao(current_user, file_to_update)
    if assoc.access_rights == AccessRights.OWNER or assoc.access_rights == AccessRights.EDITOR:
        full_file_path = os.path.join(file_to_update.filepath, str(file_to_update.id))
        shutil.copyfileobj(temp_file.file, open(full_file_path, "wb"))

        file_size = os.path.getsize(full_file_path)
        update_file_size_dao(file_to_update.id, file_size)

        return get_file_by_id_dao(file_to_update.id)
    else:
        raise ForbiddenException()


async def rename_file_service(file_id: uuid.UUID, file_rename: FileSchema, user: UserDb):
    found = False
    for assoc in get_user_files_assoc_dao(user):
        if assoc.file.id == file_id:
            found = True
            if assoc.access_rights == AccessRights.OWNER or assoc.access_rights == AccessRights.EDITOR:
                rename_file_by_id_dao(assoc.file.id, file_rename.filename)
            else:
                raise ForbiddenException()

    if not found:
        raise NotFoundException()


async def share_file_service(file_id: uuid.UUID, current_user: UserDb, permissions: List[Permission]):
    file_schema = get_file_by_id_dao(file_id)
    assoc = get_assoc_dao(current_user, file_schema)

    if assoc.access_rights != AccessRights.OWNER:
        raise ForbiddenException()

    for permission in permissions:
        shared_user_schema = get_user_by_username_dao(permission.username)
        link_user_file_dao(shared_user_schema, file_schema, permission.permission)


async def revoke_file_service(file_id: uuid.UUID, current_user: UserDb, usernames: List[str]):
    file_schema = get_file_by_id_dao(file_id)
    assoc = get_assoc_dao(current_user, file_schema)

    if assoc.access_rights != AccessRights.OWNER:
        raise ForbiddenException()

    for username in usernames:
        revoke_user_schema = get_user_by_username_dao(username)
        unlink_user_file_dao(revoke_user_schema, file_schema)


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
                raise ForbiddenException()

    if not found:
        raise NotFoundException()
