import traceback
from http import HTTPStatus

from fastapi import Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from internal.service.services import Services, new_services


def DefaultErrorHandler(err: HTTPStatus, details=None, request=None):
    content = {"message": err.phrase, "details": details, "request": request}
    return JSONResponse(status_code=err.value, content=content)


async def ValidationErrorHandler(req: Request, exc: RequestValidationError):
    err = HTTPStatus.UNPROCESSABLE_ENTITY
    data = None
    body = await req.body()
    if body:
        data = await req.json()

    return DefaultErrorHandler(err, exc.errors(), data)


def GeneralExceptionHandler(req: Request, exc: StarletteHTTPException):
    request_data = {"query": str(req.url.query), "method": req.method, "path_parameters": req.path_params}

    if exc.status_code == 400:
        return DefaultErrorHandler(err=HTTPStatus.BAD_REQUEST, details=exc.detail, request=request_data)
    elif exc.status_code == 404:
        return DefaultErrorHandler(err=HTTPStatus.NOT_FOUND, request=request_data)
    elif exc.status_code == 405:
        return DefaultErrorHandler(err=HTTPStatus.METHOD_NOT_ALLOWED, request=request_data)
    elif exc.status_code == 500:
        return InternalServerHandler(req, exc)


def InternalServerHandler(req: Request, exc: Exception, services: Services = Depends(new_services)):
    services.loggers.errorLog.error(f"Error: {exc}\nTraceback: {traceback.format_exc()}")
    err = HTTPStatus.INTERNAL_SERVER_ERROR
    content = {"message": err.phrase, "details": str(exc)}

    return JSONResponse(status_code=err.value, content=content)
