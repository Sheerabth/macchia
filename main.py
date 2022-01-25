from fastapi import FastAPI

from api.router import file
from config import Config

Config.configure()

app = FastAPI()

app.include_router(file.router, prefix="/file")

