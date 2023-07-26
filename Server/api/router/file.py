from uuid import UUID, uuid4
from typing import Optional
import os
import urllib

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, RedirectResponse

import api.service.file as file_service
import gzip
from core.schemas.file import File, FileInDb

from core.schemas.user import UserDb, User
from core.auth.auth import get_current_user

from starlette.requests import Request
from core.schemas.permission import Permission

from core.middleware.redirect_middleware import redirect_middleware

router = APIRouter()


@router.post("/{file_name}", response_model=FileInDb)
async def new_file(file_name: str, file: Request, file_id: Optional[UUID] = None, current_user: UserDb = Depends(get_current_user)):
    if not file_id:
        file_id = uuid4()
        redirect_host = await redirect_middleware(file_id)
        if redirect_host:
            host, port = redirect_host
            new_url = file.url.replace(hostname=host, port=port).include_query_params(file_id=file_id)
            print("New URL: ", new_url)
            return RedirectResponse(new_url)

    created_file = await file_service.create_file_service(file_name, file, current_user, file_id)
    return created_file


@router.get("/{file_id}")
async def download_file(file_id: UUID, req: Request, current_user: UserDb = Depends(get_current_user), redirect_host=Depends(redirect_middleware)):
    if redirect_host:
        host, port = redirect_host
        new_url = req.url.replace(hostname=host, port=port)
        return RedirectResponse(new_url)

    file = await file_service.get_file_by_id_service(file_id, current_user)

    def file_stream_generator(file_to_stream, block_size):
        full_file_path = os.path.join(file_to_stream.filepath, str(file_to_stream.id))

        with gzip.open(full_file_path, 'rb') as f:
            while True:
                content = f.read(block_size)
                if not content:
                    break
                yield content

    encoded_filename = urllib.parse.quote(file.filename)
    return StreamingResponse(file_stream_generator(file, 8192),
                             headers={"Content-Disposition": f"attachment; filename={encoded_filename}"})


@router.put("/{file_id}")
async def update_file(file_id: UUID, file: Request, current_user: UserDb = Depends(get_current_user), redirect_host=Depends(redirect_middleware)):
    if redirect_host:
        host, port = redirect_host
        new_url = file.url.replace(hostname=host, port=port)
        return RedirectResponse(new_url)

    await file_service.update_file_service(file_id, file, current_user)


@router.put("/share/{file_id}")
async def share_file(file_id: UUID, permission: Permission, current_user: UserDb = Depends(get_current_user)):
    await file_service.share_file_service(file_id, current_user, permission)


@router.put("/revoke/{file_id}")
async def revoke_file(file_id: UUID, revoked_user: User, current_user: UserDb = Depends(get_current_user)):
    await file_service.revoke_file_service(file_id, current_user, revoked_user)


@router.put("/rename/{file_id}")
async def rename_file(file_id: UUID, file_rename: File, current_user: UserDb = Depends(get_current_user)):
    await file_service.rename_file_service(file_id, file_rename, current_user)


@router.delete("/{file_id}")
async def delete_file(file_id: UUID, req: Request, current_user: UserDb = Depends(get_current_user), redirect_host=Depends(redirect_middleware)):
    if redirect_host:
        host, port = redirect_host
        new_url = req.url.replace(hostname=host, port=port)
        return RedirectResponse(new_url)

    await file_service.delete_file_by_id_service(file_id, current_user)
