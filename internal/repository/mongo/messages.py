from datetime import datetime

from bson import ObjectId

from internal.repository.models.exceptions import NotFoundException, BadRequestException


class MessageRepository:
    def __init__(self, db):
        self.db = db["messages"]

    def Create(self, content: str, from_user_id: int, to_user_id: int):
        document = {
            "content": content,
            "from_user_id": from_user_id,
            "to_user_id": to_user_id,
            "publish_timestamp": datetime.utcnow().timestamp(),  # Default to current UNIX timestamp
        }

        # Insert the document into the collection
        result = self.db.insert_one(document)

        # Return the generated _id
        return str(result.inserted_id)

    def ReadByID(self, id: str):
        try:
            object_id = ObjectId(id)
        except Exception:
            raise BadRequestException

        message = self.db.find_one({"_id": object_id})
        if not message:
            raise NotFoundException

        message["_id"] = str(message["_id"])
        return message

    def ReadAllByFromToID(self, from_user_id: int, to_user_id: int):
        cursor = self.db.find(
            {"from_user_id": from_user_id, "to_user_id": to_user_id}
        ).sort("publish_timestamp", -1)  # Sort by publish_timestamp descending

        # Retrieve all matching documents
        messages = cursor.to_list(length=None)
        for message in messages:
            message["_id"] = str(message["_id"])

        return messages

    def Update(self, id: str, content: str, from_user_id: int, to_user_id: int):
        new_data = {
            "$set": {
                "content": content,
                "from_user_id": from_user_id,
                "to_user_id": to_user_id,
                "edit_timestamp": datetime.utcnow().timestamp()  # Set current timestamp
            }
        }

        self.db.update_one({"_id": ObjectId(id)}, new_data)

    def Delete(self, id: str):
        self.db.delete_one({"_id": ObjectId(id)})
