import os

from dotenv import load_dotenv


class Config:
    configured = False

    STORAGE_DIR = None

    DATABASE_NAME = None
    DATABASE_USER = None
    DATABASE_PASSWORD = None
    DATABASE_HOST = None
    DATABASE_PORT = None

    SECRET_KEY = None
    ALGORITHM = None
    ACCESS_TOKEN_EXPIRE_MINUTES = None

    @staticmethod
    def configure():
        if not Config.configured:
            load_dotenv()

            Config.STORAGE_DIR = os.getenv("STORAGE_DIR")

            Config.DATABASE_NAME = os.getenv("DATABASE_NAME")
            Config.DATABASE_USER = os.getenv("DATABASE_USER")
            Config.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
            Config.DATABASE_HOST = os.getenv("DATABASE_HOST")
            Config.DATABASE_PORT = os.getenv("DATABASE_PORT")

            Config.SECRET_KEY = os.getenv("SECRET_KEY")
            Config.ALGORITHM = os.getenv("ALGORITHM")
            Config.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

            Config.configured = True



