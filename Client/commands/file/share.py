from exceptions.server import ServerException
from web.file import share_file
from session.user_files import UserFiles
import typer
import json


def share():
    """
    Share a file in the blob storage to another user
    If already shared, the newly specified permission overwrites the existing permission
    """
    selected_file = UserFiles.prompt_file()

    username = typer.prompt("Enter username to share with")
    permissions = {"O": "OWNER", "E": "EDITOR", "V": "VIEWER"}

    while True:
        permission = typer.prompt("Enter access permission (O - OWNER, E - EDITOR, V - VIEWER)")

        permission = permission.upper()
        if permission not in permissions.keys():
            typer.echo(typer.style("Invalid input, enter one of O/E/V", fg=typer.colors.RED, bold=True))
        else:
            break

    resp = share_file(selected_file['id'], username, permissions[permission])

    if resp.status_code != 200:
        raise ServerException(json.loads(resp.text)["detail"])
