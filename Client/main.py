import sys

import typer
from click_repl import repl

from exceptions.base import Base

from commands.auth.register import register_user as register
from commands.auth.login import login_user as login
from commands.file.ls import ls

from config import Config
Config.configure()

app = typer.Typer()

app.command(name="register")(register)
app.command(name="login")(login)
app.command(name="ls")(ls)


@app.command()
def myrepl(ctx: typer.Context):
    # while True:
    try:
        repl(ctx)
    except Base as b:
        err = typer.style(str(b), fg=typer.colors.RED, bold=True)
        typer.echo(err)


if __name__ == "__main__":
    app()
