from fastapi import FastAPI
import uvicorn

from api.router import file
from config import Config


Config.configure()

app = FastAPI()

app.include_router(file.router, prefix="/file")

uvicorn.run(app, host="0.0.0.0", port=4567)
