import json
import typer

from exceptions.server import ServerException
from session.user_files import UserFiles
from web.file import rename_file


def rename():
    selected_file = UserFiles.prompt_file()

    new_name = typer.prompt("Enter new name of file")
    resp = rename_file(selected_file['id'], new_name)

    if resp.status_code != 200:
        raise ServerException(json.loads(resp.text)["detail"])
