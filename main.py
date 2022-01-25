from fastapi import FastAPI
from api.router import file
from dotenv import load_dotenv

from config import Config
Config.configure()

app = FastAPI()

app.include_router(file.router, prefix="/file")


@app.get("/")
def get_home():
    return {"Hello": "World"}
