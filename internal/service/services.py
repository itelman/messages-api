from fastapi import Depends

from internal.config.logger import Logger, loggers
from internal.service.message.message import MessageService
from pkg.store.mongo import NewMongoDB


class Services:
    message_service: MessageService
    loggers: Logger

    def __init__(self, logger: Logger):
        self.loggers = logger

    def __call__(self, db=Depends(NewMongoDB)):
        self.db_session = db
        self.message_service = MessageService(db)

        return self


new_services = Services(loggers)
