from enum import IntEnum

class ERROR_CODES(IntEnum):
    # 4xx Client Errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    TOO_MANY_REQUESTS = 429

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

    # Custom Domain Errors
    USER_ALREADY_EXISTS = 1002
    USER_NOT_FOUND = 1003
    INVALID_CREDENTIALS = 1004
