"""API exceptions

Exceptions that should be raised when the API is used incorrectly.
"""


class BadRequestException(Exception):
    """
    This exception should be raised when the request performed by the client is
    incorrect (HTTP Bad Request 400).
    """
    status_code = 400

    def __init__(self, message, ):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        rv = {}
        rv["status"] = "error"
        rv["message"] = self.message
        return rv
