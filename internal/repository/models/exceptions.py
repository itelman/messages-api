from http import HTTPStatus

from starlette.exceptions import HTTPException as StarletteHTTPException


class BadRequestException(StarletteHTTPException):
    def __init__(self, msg: str = HTTPStatus.BAD_REQUEST.phrase):
        err = HTTPStatus.BAD_REQUEST
        super().__init__(status_code=err.value, detail=msg)


class NotFoundException(StarletteHTTPException):
    def __init__(self):
        err = HTTPStatus.NOT_FOUND
        super().__init__(status_code=err.value, detail=err.phrase)


BadRequestExceptionDefault = BadRequestException()
NotFoundException = NotFoundException()
