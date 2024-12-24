# Messages REST API

## Description

This API manages messages in MongoDB Database.

Tech Stack: FastAPI, MongoDB, Pydantic, WebSocket, Docker.

## How to run

Use the link: [https://messages-api-10gq.onrender.com](https://messages-api-10gq.onrender.com)

Or...

1. Clone repo:

```shell
git clone https://github.com/itelman/messages-api.git
```

2. Open repo:

```shell
cd messages-api
```

3. Run the repo:

```shell
fastapi dev main.py
```

## Endpoints

### Service: Messages

- **Endpoint: /api/messages --> CREATE MESSAGE**:
    - Method: POST
    - Type: JSON
    - Request:
  ```json
  {
    "content": <str>,
    "from_user_id": <int>,
    "to_user_id": <int>
  }
  ```
    - Response:
  ```json
  {
    "id": <str>
  }
  ```

- **Endpoint: /api/messages/{id} --> GET MESSAGE BY ID**:
    - Method: GET
    - Response:
  ```json
  {
    "_id": <str>,
    "content": <str>,
    "from_user_id": <int>,
    "to_user_id": <int>,
    "publish_timestamp": <float>,
    "edit_timestamp": <float> or <null>
  }
  ```

- **Endpoint: /api/messages?from_user_id={int}&to_user_id={int} --> GET ALL MESSAGES BY FROM_USER_ID & TO_USER_ID**:
    - Method: GET
    - Response:
  ```json
  [
  {
    "_id": <str>,
    "content": <str>,
    "from_user_id": <int>,
    "to_user_id": <int>,
    "publish_timestamp": <float>,
    "edit_timestamp": <float>
  },
  ...
  ]
  ```

- **Endpoint: /api/messages/{id} --> UPDATE MESSAGE**:
    - Method: PUT
    - Type: JSON
    - Request:
  ```json
  {
    "content": <str>,
    "from_user_id": <int>,
    "to_user_id": <int>
  }
  ```
    - Response:
  ```json
  {
    "id": <str>
  }
  ```

- **Endpoint: /api/messages/{id} --> DELETE MESSAGE**:
    - Method: DELETE
    - Response:
  ```json
  {
    "id": <str>
  }
  ```

- **Endpoint: /api/chat --> GET RANDOM MESSAGE FROM WEBSOCKET CONNECTION EACH SECOND**:
    - Connection:
      WebSocket --> [ws://messages-api-10gq.onrender.com/api/chat](ws://messages-api-10gq.onrender.com/api/chat)
    - Response:
  ```json
  {
    "_id": <str>,
    "content": <str>,
    "from_user_id": <int>,
    "to_user_id": <int>,
    "publish_timestamp": <float>,
    "edit_timestamp": <float>
  }
  ```

## Errors

- **400 (Bad Request) / 404 (Not Found) / 405 (Method Not Allowed) / 422 (Unprocessable Entity)**:
  ```json
  {
    "message": <str>,
    "details": <str> or <dict>,
    "request": <dict> or <null>
  }
  ```

- **500 (Internal Server)**:
  ```json
  {
    "message": <str>,
    "details": <str>
  }
  ```