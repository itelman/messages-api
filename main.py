import asyncio

from dotenv import load_dotenv
from fastapi import Depends
from fastapi import FastAPI, WebSocket
from fastapi import WebSocketDisconnect
from fastapi.exceptions import RequestValidationError
from pymongo.errors import CollectionInvalid
from starlette.exceptions import HTTPException as StarletteHTTPException

from internal.config.logger import loggers
from internal.handlers.exceptions import ValidationErrorHandler, GeneralExceptionHandler
from internal.service.services import Services, new_services
from internal.validation.request_body import RequestBody
from pkg.middleware.request_log import RequestLoggingMiddleware
from pkg.store.mongo import NewMongoDB

app = FastAPI()

load_dotenv()


@app.on_event("startup")
async def startup_event():
    try:
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

        try:
            db = NewMongoDB()
            db.create_collection("messages", validator=validator)
            loggers.infoLog.info("Collection 'messages' created successfully.")
        except CollectionInvalid:
            loggers.infoLog.info("Collection 'messages' already exists.")

    except Exception as e:
        loggers.errorLog.error(f"Error creating collection: {e}")


app.add_middleware(RequestLoggingMiddleware, services=new_services)

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


@app.websocket(api_url + "/chat")
async def websocket_endpoint(websocket: WebSocket, db=Depends(NewMongoDB)):
    messages_collection = db["messages"]
    await websocket.accept()

    try:
        while True:
            random_message = messages_collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)

            if random_message:
                message = random_message[0]

                # await websocket.send_text(message["content"])

                message["_id"] = str(message["_id"])
                await websocket.send_json(message)

            await asyncio.sleep(1)
    except WebSocketDisconnect:
        loggers.infoLog.info("Client disconnected")
    except Exception as e:
        raise e
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            loggers.infoLog.info("WebSocket was already closed.")
