class BlobStorageBaseException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        print("Status code set")
        super(Exception, self).__init__(message)

