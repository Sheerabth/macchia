from session.user_session import UserSession
import typer


def logout():
    UserSession.logout()
    typer.echo("Logged out successfully")
