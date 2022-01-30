from session.user_session import UserSession
from config import Config
import os
import click_spinner


def download_file(file_id, file_name):
    session = UserSession.get_session()

    local_filename = os.path.join(Config.DOWNLOAD_LOCATION, file_name)

    req_url = Config.SERVER_URL + "/file/" + file_id
    with session.get(req_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            with click_spinner.spinner():
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)


def upload_file(file_path: str):
    file_name = os.path.basename(file_path)
    # files = {'file': open(file_path, 'rb')}

    session = UserSession.get_session()
    with click_spinner.spinner():
        with open(file_path, 'rb') as file:
            resp = session.post(Config.SERVER_URL + f"/file/{file_name}", data=file)

    return resp


def rename_file(file_id, new_name):
    session = UserSession.get_session()
    json_body = {"filename": new_name}
    resp = session.put(Config.SERVER_URL + f"/file/rename/{file_id}", json=json_body)
    return resp


def delete_file(file_id):
    session = UserSession.get_session()

    resp = session.delete(Config.SERVER_URL + f"/file/{file_id}")
    return resp


def update_file(file_path: str, file_id):
    files = {'file': open(file_path, 'rb')}

    session = UserSession.get_session()
    with click_spinner.spinner():
        resp = session.put(Config.SERVER_URL + f"/file/{file_id}", files=files)
    return resp


def share_file(file_id, username, permission):
    json_req = {"username": username, "permission": permission}

    session = UserSession.get_session()
    resp = session.put(Config.SERVER_URL + f"/file/share/{file_id}", json=json_req)

    return resp


def revoke_file(file_id, username):
    json_req = {"username": username}

    session = UserSession.get_session()
    resp = session.put(Config.SERVER_URL + f"/file/revoke/{file_id}", json=json_req)

    return resp
