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

    LOGGER_CONF = None

    SERVER_IP = None
    SERVER_PORT = None

    NODE_ID = None

    RABBITMQ_HOST = None
    TOTAL_NODES = None

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

            Config.LOGGER_CONF = os.getenv("LOGGER_CONF")

            Config.SERVER_IP = os.getenv("SERVER_IP")
            Config.SERVER_PORT = int(os.getenv("SERVER_PORT"))
            Config.NODE_ID = os.getenv('NODE_ID')

            Config.RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
            Config.TOTAL_NODES = int(os.getenv("TOTAL_NODES"))

            Config.configured = True



