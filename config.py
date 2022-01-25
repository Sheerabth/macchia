from dotenv import load_dotenv
import os


class Config:
    STORAGE_DIR = None

    @staticmethod
    def configure():
        load_dotenv()

        Config.STORAGE_DIR = os.getenv("STORAGE_DIR")


