from web.file import download_file
from session.user_files import UserFiles


def get():
    """
    Download a file from the blob storage to the local device
    """
    selected_file = UserFiles.prompt_file()

    download_file(selected_file['id'], selected_file['filename'])
