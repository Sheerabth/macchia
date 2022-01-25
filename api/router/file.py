from fastapi import APIRouter, UploadFile
from api.service import file as file_service

router = APIRouter()


@router.post("/{file_name}")
async def new_file(file_name: str, file: UploadFile):
    await file_service.create_file(file_name, file)


@router.get("/{file_name}")
async def get_file(file_name: str):
    response = await file_service.get_file(file_name)
    return response
