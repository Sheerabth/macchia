import sys

import typer
from click_repl import repl

from exceptions.base import Base

from commands.auth.register import register_user as register
from commands.auth.login import login_user as login
from commands.auth.logout import logout

from commands.file.ls import ls
from commands.file.get import get
from commands.file.put import put
from commands.file.rename import rename
from commands.file.delete import delete
from commands.file.share import share
from commands.file.revoke import revoke
from commands.file.update import update

import utils

from config import Config
Config.configure()

app = typer.Typer()

app.command(name="register")(register)
app.command(name="login")(login)
app.command(name="logout")(logout)

app.command(name="ls")(ls)
app.command(name="get")(get)
app.command(name="put")(put)
app.command(name="rename")(rename)
app.command(name="delete")(delete)
app.command(name="share")(share)
app.command(name="revoke")(revoke)
app.command(name="update")(update)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        repl(ctx)


if __name__ == "__main__":
    utils.echo_success("Welcome to Blob-Storage CLI!")
    typer.echo("Use Ctrl + D to exit from this prompt")
    typer.echo("--help lists all available commands")

    while True:
        try:
            app()
        except Base as b:
            utils.echo_error(str(b))
        except BaseException as be:
            typer.echo(be)
            break

