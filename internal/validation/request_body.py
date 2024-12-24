from pydantic import BaseModel


class RequestBody(BaseModel):
    content: str
    from_user_id: int
    to_user_id: int


class RequestBodyValidation:
    def __init__(self, body: RequestBody):
        self.body = body
        self.errors = []

    def ContentExists(self):
        if not self.body.content.strip():
            self.errors.append("Content is empty")

    def AreUsersUnique(self):
        if self.body.from_user_id == self.body.to_user_id:
            self.errors.append("User cannot send messages to themselves")

    def Validate(self):
        self.ContentExists()
        self.AreUsersUnique()
