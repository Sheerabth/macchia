import json
import typer
from pathlib import Path

from exceptions.server import ServerException
from web.file import upload_file


def put(file_path: Path = typer.Argument(...,
                                         exists=True,
                                         file_okay=True,
                                         dir_okay=False,
                                         readable=True,
                                         resolve_path=True,
                                         help="The path of the file to be uploaded"
                                         )):
    """
    Upload a file from the local device to the blob storage
    """
    resp = upload_file(str(file_path))

    if resp.status_code != 200:
        raise ServerException(json.loads(resp.text)["detail"])
