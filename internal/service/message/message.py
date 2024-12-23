from internal.repository.models.exceptions import BadRequestException
from internal.repository.mongo.messages import MessageRepository
from internal.validation.request_body import RequestBody


class MessageService:
    def __init__(self, db):
        self.message_repository = MessageRepository(db)

    def Create(self, req: RequestBody) -> str:
        if not req.ContentExists():
            raise BadRequestException

        content, from_user_id, to_user_id = req.content, req.from_user_id, req.to_user_id

        id = self.message_repository.Create(content, from_user_id, to_user_id)
        return id

    def Get(self, id: str):
        message = self.message_repository.ReadByID(id)
        return message

    def GetAllByFromToID(self, from_user_id: int, to_user_id: int):
        messages = self.message_repository.ReadAllByFromToID(from_user_id, to_user_id)
        return messages

    def Update(self, id: str, req: RequestBody):
        if not req.ContentExists():
            raise BadRequestException
        
        try:
            self.Get(id)
        except Exception as err:
            raise err

        content, from_user_id, to_user_id = req.content, req.from_user_id, req.to_user_id
        self.message_repository.Update(id, content, from_user_id, to_user_id)

    def Delete(self, id: str):
        try:
            self.Get(id)
        except Exception as err:
            raise err

        self.message_repository.Delete(id)
