from http import HTTPStatus


class ApiError(Exception):
    code = HTTPStatus.UNPROCESSABLE_ENTITY

    def __init__(self, description=None):
        self.description = description


class BadRequest(ApiError):
    code = HTTPStatus.BAD_REQUEST


class Unauthorized(ApiError):
    code = HTTPStatus.UNAUTHORIZED


class Forbidden(ApiError):
    code = HTTPStatus.FORBIDDEN


class NotFound(ApiError):
    code = HTTPStatus.NOT_FOUND


class PreconditionFailed(ApiError):
    code = HTTPStatus.PRECONDITION_FAILED

class Unavailable(ApiError):
    code = HTTPStatus.SERVICE_UNAVAILABLE