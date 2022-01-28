import typer
from web.auth import register_user_req


def register_user(username: str = typer.Option(..., prompt=True),
                  password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True)):
    resp = register_user_req(username, password)
    print(resp.status_code)
