# Take a HTTP response object and translate it into an Exception
# instance.
def handle_error_response(resp):
    # Mapping of API response codes to exception classes
    codes = {
        400: ValidationError,
        401: UnauthorizedError,
        403: ForbiddenError,
        404: NotFound,
        429: TooManyRequests,
        500: InternalServerError,
        502: BadGateway,
        503: ServiceUnavailable,
    }

    error = resp.json().get('error', {})
    message = error.get('error_description')
    code_name = error.get('code_name', "")
    code = resp.status_code
    data = resp.json().get('data', {})

    # Build the appropriate exception class with as much
    # data as we can pull from the API response and raise
    # it.
    raise codes[code](message=message, code=code, code_name=code_name, data=data, response=resp)


class SpotifyAPIError(Exception):
    response = None
    data = {}
    code = ""
    code_name = ""
    message = "An unknown error occurred"

    def __init__(self, message=None, code=None, code_name=None, data=None, response=None):
        self.response = response
        if message:
            self.message = message
        if code:
            self.code = code
        if code_name:
            self.code_name = code_name
        if data:
            self.data = data

    def __str__(self):
        if self.code:
            return '{}: {}'.format(self.code, self.message)
        return self.message

# Specific exception classes


class ValidationError(SpotifyAPIError):
    pass


class UnauthorizedError(SpotifyAPIError):
    pass


class ForbiddenError(SpotifyAPIError):
    pass


class NotFound(SpotifyAPIError):
    pass


class TooManyRequests(SpotifyAPIError):
    pass


class InternalServerError(SpotifyAPIError):
    pass


class BadGateway(SpotifyAPIError):
    pass


class ServiceUnavailable(SpotifyAPIError):
    pass
