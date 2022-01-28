class Base(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        super(Exception, self).__init__(message)

