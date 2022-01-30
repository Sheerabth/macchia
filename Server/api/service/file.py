import os
from tempfile import TemporaryFile

import uuid
import api.dao.file as file_dao
import api.dao.user as user_dao
from config import Config

from core.database.models.access_rights_enum import AccessRights

from core.schemas.file import File as FileSchema, FileInDb
from core.schemas.permission import Permission
from core.schemas.user import User, UserDb

from core.exceptions import NotFoundException, ForbiddenException, BadRequestException

import shutil
import gzip
from starlette.requests import Request


async def create_file_service(file_name: str, file: Request, user: UserDb) -> FileInDb:
    created_file = file_dao.create_file_dao(FileSchema(filename=file_name), Config.STORAGE_DIR, -1)
    file_dao.link_user_file_dao(user, created_file, AccessRights.OWNER)

    full_file_path = os.path.join(Config.STORAGE_DIR, str(created_file.id))
    # shutil.copyfileobj(temp_file.file, gzip.open(full_file_path, "wb"))

    compressed_file = gzip.open(full_file_path, "wb")
    async for chunk in file.stream():
        compressed_file.write(chunk)

    file_size = os.path.getsize(full_file_path)
    file_dao.update_file_size_dao(created_file.id, file_size)

    return file_dao.get_file_by_id_dao(created_file.id)


async def get_file_by_id_service(file_id: uuid.UUID, user: UserDb) -> FileInDb:
    user_files = user_dao.get_user_files_dao(user)
    print(user_files)
    for file in user_files:
        if file.id == file_id:
            return file

    raise NotFoundException()


async def update_file_service(file_id: uuid.UUID, temp_file: TemporaryFile, current_user: UserDb):
    file_to_update = file_dao.get_file_by_id_dao(file_id)

    assoc = user_dao.get_assoc_dao(current_user, file_to_update)
    if assoc.access_rights == AccessRights.OWNER or assoc.access_rights == AccessRights.EDITOR:
        full_file_path = os.path.join(file_to_update.filepath, str(file_to_update.id))
        shutil.copyfileobj(temp_file.file, gzip.open(full_file_path, "wb"))

        file_size = os.path.getsize(full_file_path)
        file_dao.update_file_size_dao(file_to_update.id, file_size)

        return file_dao.get_file_by_id_dao(file_to_update.id)
    else:
        raise ForbiddenException()


async def rename_file_service(file_id: uuid.UUID, file_rename: FileSchema, user: UserDb):
    found = False
    for assoc in user_dao.get_user_files_assoc_dao(user):
        if assoc.file.id == file_id:
            found = True
            if assoc.access_rights == AccessRights.OWNER or assoc.access_rights == AccessRights.EDITOR:
                file_dao.rename_file_by_id_dao(assoc.file.id, file_rename.filename)
            else:
                raise ForbiddenException()

    if not found:
        raise NotFoundException()


async def share_file_service(file_id: uuid.UUID, current_user: UserDb, permission: Permission):
    file_schema = file_dao.get_file_by_id_dao(file_id)
    assoc = user_dao.get_assoc_dao(current_user, file_schema)

    if not assoc:
        raise NotFoundException()

    if assoc.access_rights != AccessRights.OWNER:
        raise ForbiddenException()

    # To check if the file has already been shared to the user
    shared_user_schema = user_dao.get_user_by_username_dao(permission.username)
    if not shared_user_schema:
        raise BadRequestException(message="The specified user does not exist")

    shared_user_assoc = user_dao.get_assoc_dao(shared_user_schema, file_schema)

    if not shared_user_assoc:
        # If not already shared, create a new entry
        file_dao.link_user_file_dao(shared_user_schema, file_schema, permission.permission)
    else:
        # If already shared, update the existing entry
        file_dao.update_permission_dao(shared_user_schema, file_schema, permission.permission)


async def revoke_file_service(file_id: uuid.UUID, current_user: UserDb, revoked_user: User):
    file_schema = file_dao.get_file_by_id_dao(file_id)
    assoc = user_dao.get_assoc_dao(current_user, file_schema)

    if not assoc:
        raise NotFoundException()

    if assoc.access_rights != AccessRights.OWNER:
        raise ForbiddenException()

    revoke_user_schema = user_dao.get_user_by_username_dao(revoked_user.username)
    if not revoke_user_schema:
        raise BadRequestException(message="The specified user does not exist")

    revoked_user_assoc = user_dao.get_assoc_dao(revoke_user_schema, file_schema)

    if not revoked_user_assoc:
        raise BadRequestException(message="Invalid revoke, file not shared to user")

    file_dao.unlink_user_file_dao(revoke_user_schema, file_schema)


async def delete_file_by_id_service(file_id: uuid.UUID, user: UserDb):
    found = False
    for assoc in user_dao.get_user_files_assoc_dao(user):
        print(assoc)
        if assoc.file.id == file_id:
            found = True
            if assoc.access_rights == AccessRights.OWNER:
                filepath = os.path.join(assoc.file.filepath, str(assoc.file_id))
                file_dao.delete_file_by_id_dao(file_id)
                os.remove(filepath)
            else:
                raise ForbiddenException()

    if not found:
        raise NotFoundException()
