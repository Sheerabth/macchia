import requests
from user_session import UserSession
from config import Config
from typing import Optional


def get_user_detail_req():
    s = UserSession.get_session()

    resp = s.get(Config.SERVER_URL + "/user/me")
    return resp


def get_user_files(pattern: Optional[str] = None):
    s = UserSession.get_session()
    if not pattern:
        resp = s.get(Config.SERVER_URL + '/user/files')
    else:
        query_params = {'pattern': pattern}
        resp = s.get(Config.SERVER_URL + '/user/files', params=query_params)
    return resp
