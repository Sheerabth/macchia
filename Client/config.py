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

            Config.configured = True



