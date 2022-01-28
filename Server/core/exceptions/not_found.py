from .base import BaseException
from fastapi import status


class NotFoundException(BaseException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, message="The requested resource was not found"):
        super(NotFoundException, self).__init__(status_code, message)
