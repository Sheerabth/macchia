from .base import BaseException
from fastapi import status


class BadRequestException(BaseException):
    def __init__(self, status_code=status.HTTP_403_FORBIDDEN, message="Bad Request"):
        super(BadRequestException, self).__init__(status_code, message)
