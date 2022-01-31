from session.user_session import UserSession
from utils import echo_success
import typer


def logout():
    """
    Log Out of the system
    """
    UserSession.logout()
    echo_success("Logged out successfully")
