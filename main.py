from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from user_actions.jwt_op import verify_token
from chat_actions.appLogic import send_message
from typing import List
from settings import origins
from fastapi.templating import Jinja2Templates
from user_actions.api import router as user_router
from chat_actions.api import router as chat_router
from vacancies.api import router as vacancies_router
import asyncio
import logging
import sys
from vacancies.telegram import main as telegram_main
import uvicorn
from multiprocessing import Process


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # send message to the list of connections
    async def broadcast(self, message: str, websocket: WebSocket):
        for connection in self.active_connections:
            if (connection == websocket):
                continue
            await connection.send_text(message)


connection_manager = ConnectionManager()


@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, decoded_token: dict = Depends(verify_token)):
    # Connect the client
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            send_message({"message": data}, chat_id, decoded_token)
            await connection_manager.send_personal_message(f"You: {data}", websocket)
            await connection_manager.broadcast(f"Client #{chat_id}: {data}")

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

app.include_router(vacancies_router, prefix="/vacancies")
app.include_router(user_router, prefix="/user")
app.include_router(chat_router, prefix="/chat")


def run_fastapi():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Start the FastAPI server in a separate process
    fastapi_process = Process(target=run_fastapi)
    fastapi_process.start()

    # Start the Telegram bot
    asyncio.run(telegram_main())

    # Wait for the FastAPI process to complete (if needed)
    fastapi_process.join()