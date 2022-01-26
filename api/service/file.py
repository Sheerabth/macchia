import os
from tempfile import TemporaryFile

from api.dao.file import create_file_dao, link_user_file
from api.service.user import get_user_by_username_service
from config import Config

from core.schemas.file import File as FileSchema
from core.database.models.access_rights_enum import AccessRights

from core.schemas.user import UserOut


async def create_file_service(file_name: str, temp_file: TemporaryFile, user: UserOut):
    created_file = create_file_dao(FileSchema(Filename=file_name), Config.STORAGE_DIR)

    link_user_file(user, created_file, AccessRights.OWNER)

    # print(created_file)
    full_file_path = os.path.join(created_file.filepath, str(created_file.id))
    contents = await temp_file.read()
    new_file = open(full_file_path, "wb")
    new_file.write(contents)


# TODO
# async def get_file_by_name(file_name: str):
#     files = list(session.query(File).filter(File.Filename == file_name))
#
#
# async def get_file(file_name: str):
#     full_file_path = os.path.join(Config.STORAGE_DIR, file_name)
#     return full_file_path
