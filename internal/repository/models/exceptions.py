from http import HTTPStatus

from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self):
        err = HTTPStatus.BAD_REQUEST
        super().__init__(status_code=err.value, detail=err.phrase)


class NotFoundException(HTTPException):
    def __init__(self):
        err = HTTPStatus.NOT_FOUND
        super().__init__(status_code=err.value, detail=err.phrase)


BadRequestException = BadRequestException()
NotFoundException = NotFoundException()
