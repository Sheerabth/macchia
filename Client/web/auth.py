import requests
from config import Config
import bcrypt

SALT = b'$2b$12$bdBHJafNn1RsuwMg.IOCG.'


def register_user_req(username: str, password: str):
    hashed_pw = str(bcrypt.hashpw(password.encode('utf-8'), SALT))

    register_url = Config.SERVER_URL + "/register"
    req_body = {'username': username, 'password': hashed_pw}
    resp = requests.post(register_url, json=req_body)
    return resp


def login_user_req(username: str, password: str):
    hashed_pw = str(bcrypt.hashpw(password.encode('utf-8'), SALT))

    login_url = Config.SERVER_URL + "/login"
    req_body = {'username': username, 'password': hashed_pw}
    resp = requests.post(login_url, data=req_body)
    return resp
