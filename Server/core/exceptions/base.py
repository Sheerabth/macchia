class BlobStorageBaseException(Exception):
    def __init__(self, status_code, message, headers=None):
        self.status_code = status_code
        super(Exception, self).__init__(message)
        self.headers = headers

