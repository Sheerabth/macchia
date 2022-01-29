import json
import typer

from exceptions.server import ServerException
from user_files import UserFiles
from web.file import delete_file


def delete():
    selected_file = UserFiles.prompt_file()

    resp = delete_file(selected_file['id'])

    if resp.status_code != 200:
        raise ServerException(json.loads(resp.text)["detail"])
