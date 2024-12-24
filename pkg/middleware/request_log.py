from fastapi import Request, FastAPI, Depends
from starlette.middleware.base import BaseHTTPMiddleware

from internal.service.services import Services, new_services


class BaseServiceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, services: Services = Depends(new_services)):
        super().__init__(app)
        self.services = services


class RequestLoggingMiddleware(BaseServiceMiddleware):
    async def dispatch(self, request: Request, call_next):
        self.services.loggers.infoLog.info(f"{request.client.host} - {request.method} {request.url}")
        response = await call_next(request)
        return response
