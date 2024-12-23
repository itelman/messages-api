from pydantic import BaseModel


class RequestBody(BaseModel):
    content: str
    from_user_id: int
    to_user_id: int

    def ContentExists(self):
        if not self.content.strip():
            return False

        return True
