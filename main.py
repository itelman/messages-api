from fastapi import Depends
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pymongo.errors import CollectionInvalid
from starlette.exceptions import HTTPException as StarletteHTTPException

from internal.handlers.exceptions import ValidationErrorHandler, GeneralExceptionHandler
from internal.service.services import Services, new_services
from internal.validation.request_body import RequestBody
from pkg.store.mongo import NewMongoDB

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    try:
        # Define the schema validation rules
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["content", "from_user_id", "to_user_id", "publish_timestamp"],
                "properties": {
                    "content": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "from_user_id": {
                        "bsonType": "int",
                        "description": "must be an integer and is required"
                    },
                    "to_user_id": {
                        "bsonType": "int",
                        "description": "must be an integer and is required"
                    },
                    "publish_timestamp": {
                        "bsonType": "double",
                        "description": "must be a UNIX timestamp and is required"
                    },
                    "edit_timestamp": {
                        "bsonType": "double",
                        "description": "must be a UNIX timestamp if provided"
                    }
                }
            }
        }

        # Create the 'messages' collection with validation
        try:
            db = NewMongoDB()
            db.create_collection("messages", validator=validator)
            print("Collection 'messages' created successfully.")
        except CollectionInvalid:
            print("Collection 'messages' already exists.")

    except Exception as e:
        print(f"Error creating collection: {e}")


app.add_exception_handler(RequestValidationError, ValidationErrorHandler)
app.add_exception_handler(StarletteHTTPException, GeneralExceptionHandler)

api_url = "/api"
messages_url = api_url + "/messages"


@app.post(messages_url)
def Create(req: RequestBody, service: Services = Depends(new_services)):
    id = service.message_service.Create(req)
    return {"id": id}


@app.get(messages_url + "/{id}")
def Get(id: str, service: Services = Depends(new_services)):
    message = service.message_service.Get(id)
    return message


@app.get(messages_url)
def GetAllFromToID(from_user_id: int, to_user_id: int, service: Services = Depends(new_services)):
    messages = service.message_service.GetAllByFromToID(from_user_id, to_user_id)
    return messages


@app.put(messages_url + "/{id}")
def Update(id: str, req: RequestBody, service: Services = Depends(new_services)):
    service.message_service.Update(id, req)
    return {"id": id}


@app.delete(messages_url + "/{id}")
def Delete(id: str, service: Services = Depends(new_services)):
    service.message_service.Delete(id)
    return {"id": id}


@app.get(api_url + "/chat")
def Chat():
    pass
