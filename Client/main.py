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

# typer_click_object = typer.main.get_command(app)
#
# typer_click_object.add_command(get, "get")
#
# if __name__ == "__main__":
#     typer_click_object()
