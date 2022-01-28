import typer
from web.user import get_user_files
from web.file import get_file
import json
from tabulate import tabulate


def get_files():
    print("Complete called")
    files = json.loads(get_user_files().text)
    return [(index + 1, file['id'], file['filename'], file['file_size']) for index, file in enumerate(files)]


def get():
    files = get_files()

    while True:
        try:
            typer.echo(tabulate(files, headers=["FileNo", "UUID", "File Name"]))
            file_num = int(typer.prompt("Enter the file number to download"))
            selected_file = files[file_num - 1]

            break
        except IndexError:
            typer.echo(typer.style("Invalid File number", fg=typer.colors.RED, bold=True))

    get_file(selected_file[1], selected_file[2], selected_file[3])


# def complete_id(ctx, args, incomplete: str):
#     print("Complete called")
#     files = json.loads(get_user_files().text)
#     return [(file['id'], file['filename']) for file in files if file['id'].startswith(str(incomplete))]
#
# @click.command()
# @click.option("--file_id", type=str, autocompletion=complete_id)
# def get(file_id: str):
#     print(file_id)
