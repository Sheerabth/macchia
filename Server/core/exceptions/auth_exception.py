from .base import BlobStorageBaseException
from fastapi import status


class AuthException(BlobStorageBaseException):
    def __init__(self,
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 message="Unauthorized",
                 headers=None):
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}

        super(BlobStorageBaseException, self).__init__(status_code, message, headers)
