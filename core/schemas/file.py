import datetime

from pydantic import BaseModel
import uuid


class File(BaseModel):
    filename: str


class FileInDb(File):
    id: uuid.UUID
    filepath: str
    file_size: int
    created_time: datetime.datetime

    class Config:
        orm_mode = True
