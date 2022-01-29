import json
from user_session import UserSession
from config import Config
from tabulate import tabulate
import typer


class UserFiles:
    user_files = []

    @staticmethod
    def refresh_files():
        session = UserSession.get_session()
        req_url = Config.SERVER_URL + "/user/files"

        resp = session.get(req_url)
        UserFiles.user_files = json.loads(resp.text)

    @staticmethod
    def prompt_file() -> dict:
        UserFiles.refresh_files()

        file_prompt_table = [(index + 1, file['id'], file['filename'])
                             for index, file in enumerate(UserFiles.user_files)]
        while True:
            try:
                typer.echo(tabulate(file_prompt_table, headers=["FileNo", "UUID", "File Name"]))
                file_num = int(typer.prompt("Enter file number"))
                selected_file_id = file_prompt_table[file_num - 1][1]
                break
            except IndexError:
                typer.echo(typer.style("Invalid File number", fg=typer.colors.RED, bold=True))

        for file in UserFiles.user_files:
            if file['id'] == selected_file_id:
                return file
