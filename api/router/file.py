from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import FileResponse

from api.service import file as file_service

from core.schemas.user import UserOut
from core.auth import get_current_user

router = APIRouter()


@router.post("/{file_name}")
async def new_file(file_name: str, file: UploadFile, current_user: UserOut = Depends(get_current_user)):
    await file_service.create_file_service(file_name, file, current_user)


@router.get("/{file_name}")
async def get_file(file_name: str):
    full_file_path = await file_service.get_file(file_name)
    return FileResponse(path=full_file_path)
