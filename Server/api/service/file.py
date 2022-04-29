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

from uvicorn.config import logger


async def create_file_service(file_name: str, file: Request, user: UserDb, file_id: uuid.UUID) -> FileInDb:
    created_file = file_dao.create_file_dao(FileSchema(filename=file_name), file_id, Config.STORAGE_DIR, -1)
    file_dao.link_user_file_dao(user, created_file, AccessRights.OWNER)
    full_file_path = os.path.join(Config.STORAGE_DIR, str(created_file.id))

    # TODO add back gzip after debugging
    # with gzip.open(full_file_path, "wb") as compressed_file:
    print(full_file_path)
    with open(full_file_path, "wb") as compressed_file:
        print('Inside with')
        async for chunk in file.stream():
            print('Streaming')
            compressed_file.write(chunk)

    file_size = os.path.getsize(full_file_path)

    file_dao.update_file_size_dao(created_file.id, file_size)

    logger.info(f"New file {file_name} with ID {created_file.id} created by user f{user.username}")

    return file_dao.get_file_by_id_dao(created_file.id)


async def get_file_by_id_service(file_id: uuid.UUID, current_user: UserDb) -> FileInDb:
    user_files = user_dao.get_user_files_dao(current_user)
    for file in user_files:
        if file.id == file_id:
            logger.info(f"User {current_user.username} starting download of {file_id}")
            return file

    raise NotFoundException()


async def update_file_service(file_id: uuid.UUID, file: Request, current_user: UserDb):
    file_to_update = file_dao.get_file_by_id_dao(file_id)

    assoc = user_dao.get_assoc_dao(current_user, file_to_update)
    if assoc.access_rights == AccessRights.OWNER or assoc.access_rights == AccessRights.EDITOR:
        full_file_path = os.path.join(file_to_update.filepath, str(file_to_update.id))

        # TODO add back gzip after debugging
        # with gzip.open(full_file_path, "wb") as compressed_file:
        with open(full_file_path, "wb") as compressed_file:
            async for chunk in file.stream():
                compressed_file.write(chunk)

        file_size = os.path.getsize(full_file_path)
        file_dao.update_file_size_dao(file_to_update.id, file_size)

        logger.info(f"File {file_id} updated by user {current_user.username}")
        return file_dao.get_file_by_id_dao(file_to_update.id)
    else:
        raise ForbiddenException(message="Permission denied, EDITOR access is required to update files")


async def rename_file_service(file_id: uuid.UUID, file_rename: FileSchema, current_user: UserDb):
    found = False
    for assoc in user_dao.get_user_files_assoc_dao(current_user):
        if assoc.file.id == file_id:
            found = True
            if assoc.access_rights == AccessRights.OWNER or assoc.access_rights == AccessRights.EDITOR:
                file_dao.rename_file_by_id_dao(assoc.file.id, file_rename.filename)
                logger.info(f"File {file_id} renamed by user {current_user.username}")
            else:
                raise ForbiddenException(message="Permission denied, EDITOR access is required to rename files")

    if not found:
        raise NotFoundException()


async def share_file_service(file_id: uuid.UUID, current_user: UserDb, permission: Permission):
    file_schema = file_dao.get_file_by_id_dao(file_id)
    assoc = user_dao.get_assoc_dao(current_user, file_schema)

    if not assoc:
        raise NotFoundException()

    if assoc.access_rights != AccessRights.OWNER:
        raise ForbiddenException(message="Permission denied, OWNER access is required to share files")

    # To check if the file has already been shared to the user
    shared_user_schema = user_dao.get_user_by_username_dao(permission.username)
    if not shared_user_schema:
        raise BadRequestException(message="The specified user does not exist")

    shared_user_assoc = user_dao.get_assoc_dao(shared_user_schema, file_schema)

    if not shared_user_assoc:
        # If not already shared, create a new entry
        file_dao.link_user_file_dao(shared_user_schema, file_schema, permission.permission)
        logger.info(f"File {file_id} shared to user {permission.username}")
    else:
        # If already shared, update the existing entry
        file_dao.update_permission_dao(shared_user_schema, file_schema, permission.permission)
        logger.info(f"File {file_id} permission of user {permission.username} updated to {permission.permission}")


async def revoke_file_service(file_id: uuid.UUID, current_user: UserDb, revoked_user: User):
    file_schema = file_dao.get_file_by_id_dao(file_id)
    assoc = user_dao.get_assoc_dao(current_user, file_schema)

    if not assoc:
        raise NotFoundException()

    if assoc.access_rights != AccessRights.OWNER:
        raise ForbiddenException(message="Permission denied, OWNER access is required to revoke shared files")

    revoke_user_schema = user_dao.get_user_by_username_dao(revoked_user.username)
    if not revoke_user_schema:
        raise BadRequestException(message="The specified user does not exist")

    revoked_user_assoc = user_dao.get_assoc_dao(revoke_user_schema, file_schema)

    if not revoked_user_assoc:
        raise BadRequestException(message="Invalid revoke, file not shared to user")

    file_dao.unlink_user_file_dao(revoke_user_schema, file_schema)
    logger.info(f"File {file_id} revoked from user {revoked_user.username}")


async def delete_file_by_id_service(file_id: uuid.UUID, current_user: UserDb):
    found = False
    for assoc in user_dao.get_user_files_assoc_dao(current_user):
        if assoc.file.id == file_id:
            found = True
            if assoc.access_rights == AccessRights.OWNER:
                filepath = os.path.join(assoc.file.filepath, str(assoc.file_id))
                file_dao.delete_file_by_id_dao(file_id)
                os.remove(filepath)
                logger.info(f"File {file_id} deleted by user {current_user.username}")
            else:
                raise ForbiddenException(message="Permission denied, OWNER access is required to delete files")

    if not found:
        raise NotFoundException()
