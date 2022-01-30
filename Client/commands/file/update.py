from session.user_files import UserFiles
from web.file import update_file
import typer
from pathlib import Path
import json

from exceptions.server import ServerException


def update(file_path: Path = typer.Argument(...,
                                            exists=True,
                                            file_okay=True,
                                            dir_okay=False,
                                            readable=True,
                                            resolve_path=True,
                                            help="The path of the file that should update the existing file"
                                            )):
    """
    Update an existing file in the blob storage with another file
    """
    selected_file = UserFiles.prompt_file()
    resp = update_file(str(file_path), selected_file['id'])

    if resp.status_code != 200:
        raise ServerException(json.loads(resp.text)["detail"])
