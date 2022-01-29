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
                                         resolve_path=True
                                         )):
    resp = upload_file(file_path)

    if resp.status_code != 200:
        raise ServerException(json.loads(resp.text)["detail"])
