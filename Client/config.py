import os

from dotenv import load_dotenv


class Config:
    configured = False

    SERVER_URL = None


    @staticmethod
    def configure():
        if not Config.configured:
            load_dotenv()

            Config.SERVER_URL = os.getenv("SERVER_URL")
            Config.DOWNLOAD_LOCATION = os.getenv("DOWNLOAD_LOCATION")

            Config.configured = True



