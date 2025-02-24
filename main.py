from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
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
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)





app.include_router(vacancies_router, prefix="/vacancies")
app.include_router(user_router, prefix="/user")
app.include_router(chat_router, prefix="/chat")


async def run_fastapi():
    port = int(os.getenv("PORT", 8080))
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    task_fastapi = asyncio.create_task(run_fastapi())
    task_telegram = asyncio.create_task(telegram_main())
    await asyncio.gather(task_fastapi, task_telegram)

if __name__ == "__main__":
    asyncio.run(main())