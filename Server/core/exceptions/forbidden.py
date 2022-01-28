from .base import BaseException
from fastapi import status


class ForbiddenException(BaseException):
    def __init__(self, status_code=status.HTTP_403_FORBIDDEN, message="The user is not permitted to "
                                                                      "access the requested resource"):
        super(ForbiddenException, self).__init__(status_code, message)
