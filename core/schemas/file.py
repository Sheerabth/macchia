from pydantic import BaseModel, Field
import uuid


class File(BaseModel):
    filename: str = Field(alias='Filename')


class FileInDb(File):
    id: uuid.UUID = Field(alias="ID")
    filepath: str = Field(alias='Filepath')

    class Config:
        orm_mode = True