import os

from dotenv import load_dotenv


class Config:
    configured = False

    SERVER_URL = None

    @staticmethod
    def configure():
        if not Config.configured:
            load_dotenv()

            url = os.getenv("SERVER_URL")
            if url.endswith("/"):
                Config.SERVER_URL = url[:-1]
            else:
                Config.SERVER_URL = url

            Config.DOWNLOAD_LOCATION = os.getenv("DOWNLOAD_LOCATION")

            Config.configured = True



