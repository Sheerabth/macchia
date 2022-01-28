import typer
from web.user import get_user_files
import json
from exceptions.server import ServerException


def ls(search_pattern: str = typer.Argument(None)):
    resp = get_user_files(search_pattern)
    json_resp = json.loads(resp.text)
    if resp.status_code != 200:
        raise ServerException(json_resp["detail"])

    for file in json_resp:
        typer.echo(file)
