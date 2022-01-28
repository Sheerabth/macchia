import requests
from user_session import UserSession
from config import Config
import os
import typer


def get_file(file_id, file_name, file_size):
    session = UserSession.get_session()

    local_filename = os.path.join(Config.DOWNLOAD_LOCATION, file_name)

    req_url = Config.SERVER_URL + "/file/" + file_id
    with session.get(req_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            with typer.progressbar(length=file_size) as progress:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    progress.update(len(chunk))