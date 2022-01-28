from .base import Base


class NotLoggedInException(Base):
    def __init__(self, message="Please login to perform this operation"):
        super(NotLoggedInException, self).__init__(message)
