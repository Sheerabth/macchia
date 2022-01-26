from pydantic import BaseModel, Field
import uuid


class User(BaseModel):
    username: str = Field(alias='Username')


class UserCreate(User):
    password: str = Field(alias='Password')

    class Config:
        orm_mode = True


class UserOut(User):
    id: uuid.UUID = Field(alias='ID')

    class Config:
        orm_mode = True
