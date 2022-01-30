import json
from exceptions.server import ServerException
from web.file import revoke_file
from session.user_files import UserFiles
import typer


def revoke():
    selected_file = UserFiles.prompt_file()

    username = typer.prompt("Enter username to revoke access")

    resp = revoke_file(selected_file['id'], username)

    if resp.status_code != 200:
        raise ServerException(json.loads(resp.text)["detail"])
