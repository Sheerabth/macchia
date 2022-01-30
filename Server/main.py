from config import Config

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from core.exceptions import BlobStorageBaseException

Config.configure()

from api.router import file, auth, user
from uvicorn.config import logger

app = FastAPI()


@app.exception_handler(BlobStorageBaseException)
async def blob_storage_exception_handler(request: Request, exception: BlobStorageBaseException):
    if hasattr(exception, 'headers'):
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


@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exception: Exception):
    logger.exception(str(exception))

app.include_router(file.router, prefix="/file")
app.include_router(user.router, prefix="/user")
app.include_router(auth.router)


uvicorn.run(app, host="0.0.0.0", port=4567, log_config=Config.LOGGER_CONF)
