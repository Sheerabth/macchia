import typer
from pathlib import Path
from web.file import upload_file


def put(file_path: Path = typer.Argument(...,
                                         exists=True,
                                         file_okay=True,
                                         dir_okay=False,
                                         readable=True,
                                         resolve_path=True
                                         )):
    upload_file(file_path)
