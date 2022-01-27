import os
import uuid
from tempfile import TemporaryFile
from typing import Union

from api.dao.file import create_file_dao, link_user_file_dao
from api.dao.user import get_user_files_dao
from api.service.user import get_user_by_username_service
from config import Config

from core.schemas.file import File as FileSchema, FileInDb
from core.database.models.access_rights_enum import AccessRights

from core.schemas.user import UserDb


async def create_file_service(file_name: str, temp_file: TemporaryFile, user: UserDb):
    contents = await temp_file.read()

    created_file = create_file_dao(FileSchema(filename=file_name), Config.STORAGE_DIR, temp_file.file.tell())

    link_user_file_dao(user, created_file, AccessRights.OWNER)
    full_file_path = os.path.join(created_file.filepath, str(created_file.id))
    new_file = open(full_file_path, "wb")
    new_file.write(contents)

    return created_file


# TODO
# async def get_file_by_name(file_name: str):
#     files = list(session.query(File).filter(File.Filename == file_name))
#
#
async def get_file_by_id(file_id: uuid.UUID, user: UserDb) -> Union[FileInDb, None]:
    user_files = get_user_files_dao(user)
    for file in user_files:
        if file.id == file_id:
            # TODO update timestamp
            return file

    return None
