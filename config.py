import os

from dotenv import load_dotenv


class Config:
    STORAGE_DIR = None

    DATABASE_NAME = None
    DATABASE_USER = None
    DATABASE_PASSWORD = None
    DATABASE_HOST = None
    DATABASE_PORT = None


    @staticmethod
    def configure():
        load_dotenv()

        Config.STORAGE_DIR = os.getenv("STORAGE_DIR")

        Config.DATABASE_NAME = os.getenv("DATABASE_NAME")
        Config.DATABASE_USER = os.getenv("DATABASE_USER")
        Config.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
        Config.DATABASE_HOST = os.getenv("DATABASE_HOST")
        Config.DATABASE_PORT = os.getenv("DATABASE_PORT")



