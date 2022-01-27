from pydantic import BaseModel, Field
import uuid


class File(BaseModel):
    filename: str


class FileInDb(File):
    id: uuid.UUID
    filepath: str

    class Config:
        orm_mode = True
