from pydantic import BaseModel
from core.database.models.access_rights_enum import AccessRights


class Permission(BaseModel):
    username: str
    permission: AccessRights
