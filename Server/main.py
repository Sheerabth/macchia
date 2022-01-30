from config import Config

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from core.exceptions import BlobStorageBaseException

Config.configure()

from api.router import file, auth, user

app = FastAPI()


@app.exception_handler(BlobStorageBaseException)
async def base_exception_handler(request: Request, exception: BlobStorageBaseException):
    if exception.headers:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
            headers=exception.headers
        )
    else:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": str(exception)},
        )

app.include_router(file.router, prefix="/file")
app.include_router(user.router, prefix="/user")
app.include_router(auth.router)


uvicorn.run(app, host="0.0.0.0", port=4567)
