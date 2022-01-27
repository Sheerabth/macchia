from pydantic import BaseModel, Field
import uuid


class User(BaseModel):
    username: str


class UserCreate(User):
    password: str

    class Config:
        orm_mode = True


class UserOut(User):
    id: uuid.UUID

    class Config:
        orm_mode = True
