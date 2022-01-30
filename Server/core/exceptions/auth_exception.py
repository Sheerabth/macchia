from .base import BlobStorageBaseException
from fastapi import status


class AuthException(BlobStorageBaseException):
    def __init__(self,
                 status_code=status.HTTP_401_UNAUTHORIZED,
                 message="Unauthorized",
                 headers=None):

        super(AuthException, self).__init__(status_code, message)
        if headers is None:
            self.headers = {"WWW-Authenticate": "Bearer"}
        else:
            self.headers = headers
