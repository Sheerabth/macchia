from .base import BlobStorageBaseException
from fastapi import status


class BadRequestException(BlobStorageBaseException):
    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, message="Bad Request"):
        super(BadRequestException, self).__init__(status_code, message)
