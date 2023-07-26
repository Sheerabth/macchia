import requests
from exceptions.login import NotLoggedInException
from config import Config
import json


class CustomSession(requests.Session):
    def should_strip_auth(self, old_url, new_url):
        return False


class UserSession:
    logged_in = False
    session = None
    user_id = None
    username = None

    @staticmethod
    def login(access_token):
        if not UserSession.logged_in:
            UserSession.session = CustomSession()
            UserSession.session.headers.update({'Authorization': f'Bearer {access_token}'})

            resp = UserSession.session.get(Config.SERVER_URL + "/user/me")
            user_details = json.loads(resp.text)

            UserSession.user_id = user_details["id"]
            UserSession.username = user_details["username"]

            UserSession.logged_in = True

    @staticmethod
    def get_session():
        if UserSession.logged_in:
            return UserSession.session
        else:
            raise NotLoggedInException()

    @staticmethod
    def logout():
        UserSession.logged_in = False
        UserSession.session = None
        UserSession.username = None
        UserSession.user_id = None
