import uuid
import os

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse

from api.service import file as file_service

from core.schemas.user import UserDb
from core.auth.auth import get_current_user

router = APIRouter()


@router.post("/{file_name}")
async def new_file(file_name: str, file: UploadFile, current_user: UserDb = Depends(get_current_user)):
    created_file = await file_service.create_file_service(file_name, file, current_user)
    return created_file

@router.get("/{file_id}")
async def download_file(file_id: uuid.UUID, current_user: UserDb = Depends(get_current_user)):
    file = await file_service.get_file_by_id(file_id, current_user)
    # TODO check if custom exception hierarchy is required
    if not file:
        raise HTTPException(status_code=404, detail="The requested file could not be found, or you do not "
                                                    "have permissions to access it")
    return FileResponse(path=os.path.join(file.filepath, str(file.id)), filename=file.filename)
