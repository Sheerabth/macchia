from config import Config

Config.configure()

from fastapi import FastAPI
import uvicorn

from api.router import file, auth, user


app = FastAPI()

app.include_router(file.router, prefix="/file")
app.include_router(user.router, prefix="/user")
app.include_router(auth.router)


uvicorn.run(app, host="0.0.0.0", port=4567)
