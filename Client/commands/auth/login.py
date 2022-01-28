import typer
from web.auth import login_user_req
from web.user import get_user_detail_req
from user_session import UserSession
from exceptions.server import ServerException

import json


def login_user(username: str = typer.Option(..., prompt=True),
               password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True)):
    resp = login_user_req(username, password)

    json_resp = json.loads(resp.text)
    if resp.status_code != 200:
        raise ServerException(json_resp["detail"])

    UserSession.login(json_resp["access_token"])
