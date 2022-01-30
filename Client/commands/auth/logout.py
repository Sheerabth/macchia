from session.user_session import UserSession
import typer


def logout():
    """
    Log Out of the system
    """
    UserSession.logout()
    typer.echo("Logged out successfully")
