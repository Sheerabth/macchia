import datetime

from pydantic import BaseModel
import uuid
from core.database.models.access_rights_enum import AccessRights


class File(BaseModel):
    filename: str


class FileInDb(File):
    id: uuid.UUID
    filepath: str
    file_size: int
    created_time: datetime.datetime

    class Config:
        orm_mode = True


class FileWithPermission(FileInDb):
    permission: AccessRights
