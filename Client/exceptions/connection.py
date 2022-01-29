from .base import Base


class ConnectionException(Base):
    def __init__(self, message="Error in connecting to server"):
        super(ConnectionException, self).__init__(message)
