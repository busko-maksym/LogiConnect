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


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)





app.include_router(vacancies_router, prefix="/vacancies")
app.include_router(user_router, prefix="/user")
app.include_router(chat_router, prefix="/chat")


def run_fastapi():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    fastapi_process = Process(target=run_fastapi)
    fastapi_process.start()

    asyncio.run(telegram_main())

    fastapi_process.join()