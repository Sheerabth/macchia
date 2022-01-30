import json
import typer
from exceptions.server import ServerException
from web.auth import register_user_req
import utils


def register_user(username: str = typer.Option(..., prompt=True),
                  password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True)):
    resp = register_user_req(username, password)

    if resp.status_code == 200:
        utils.echo_success("Registration successful")
    else:
        raise ServerException(json.loads(resp.text)["detail"])
