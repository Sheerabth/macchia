from uuid import UUID
import os

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse

from api.service import file as file_service
from api.service.file import *
from core.schemas.file import File

from core.schemas.user import UserDb
from core.auth.auth import get_current_user

from typing import List
from core.schemas.permission import Permission

router = APIRouter()


@router.post("/{file_name}")
async def new_file(file_name: str, file: UploadFile, current_user: UserDb = Depends(get_current_user)):
    created_file = await file_service.create_file_service(file_name, file, current_user)
    return created_file


@router.get("/{file_id}")
async def download_file(file_id: UUID, current_user: UserDb = Depends(get_current_user)):
    file = await file_service.get_file_by_id_service(file_id, current_user)
    # TODO check if custom exception hierarchy is required
    if not file:
        raise HTTPException(status_code=404, detail="The requested file could not be found, or you do not "
                                                    "have permissions to access it")
    return FileResponse(path=os.path.join(file.filepath, str(file.id)), filename=file.filename)


@router.put("/share/{file_id}")
async def share_file(file_id: UUID, permissions: List[Permission], current_user: UserDb = Depends(get_current_user)):
    # print(permissions)
    await share_file_service(file_id, current_user, permissions)


# @router.put("/unshare/{file_id}")
# async def unshare_file(file_id: UUID, usernames: List[str], current_user: UserDb = Depends(get_current_user())):
#     pass

@router.put("/rename/{file_id}")
async def rename_file(file_id: UUID, file_rename: File, current_user: UserDb = Depends(get_current_user)):
    await rename_file_service(file_id, file_rename, current_user)


@router.delete("/{file_id}")
async def delete_file(file_id: UUID, current_user: UserDb = Depends(get_current_user)):
    await delete_file_by_id_service(file_id, current_user)
