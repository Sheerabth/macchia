import typer
from web.auth import login_user_req
from session.user_session import UserSession
from exceptions.server import ServerException

import utils
import json


def login_user(username: str = typer.Option(...,
                                            prompt=True),
               password: str = typer.Option(...,
                                            prompt=True,
                                            confirmation_prompt=True,
                                            hide_input=True)):
    """
    Log In by providing a username and password
    """
    resp = login_user_req(username, password)

    json_resp = json.loads(resp.text)
    if resp.status_code != 200:
        raise ServerException(json_resp["detail"])

    UserSession.login(json_resp["access_token"])
    utils.echo_success("Login successful")
