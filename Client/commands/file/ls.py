import typer
from web.user import get_user_files
import json
from exceptions.server import ServerException
from tabulate import tabulate
from dateutil import parser
from humanize import naturalsize


def ls(search_pattern: str = typer.Argument(None,
                                            help="Search pattern to match with file names while searching"),
       long_list: bool = typer.Option(False,
                                      "-l",
                                      help="Display additional details about files")):
    """
    List all accessible files
    """
    resp = get_user_files(search_pattern)
    json_resp = json.loads(resp.text)
    if resp.status_code != 200:
        raise ServerException(json_resp["detail"])

    if not long_list:
        for file in json_resp:
            typer.echo(file["filename"])
    else:
        fields = ["id", "filename", "file_size", "created_time", "permission"]
        file_table = []

        for d in json_resp:
            d["file_size"] = naturalsize(d["file_size"])
            d["created_time"] = parser.parse(d["created_time"]).strftime("%d %b %Y %H:%M")

        for d in json_resp:
            file_table.append(tuple([d[x] for x in fields]))

        typer.echo(tabulate(file_table, ["ID", "Name", "Size", "Creation Time", "Permissions"]))

