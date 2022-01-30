import json

from exceptions.server import ServerException
from session.user_files import UserFiles
from web.file import delete_file


def delete():
    """
    Delete a file from the system
    """
    selected_file = UserFiles.prompt_file()

    resp = delete_file(selected_file['id'])

    if resp.status_code != 200:
        raise ServerException(json.loads(resp.text)["detail"])
