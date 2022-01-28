from .base import Base


class ServerException(Base):
    def __init__(self, message="The operation could not be performed as the server returned an error"):
        super(ServerException, self).__init__(message)
