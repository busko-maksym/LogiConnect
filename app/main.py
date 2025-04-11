from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.v1.user import router as user_router
from app.v1.chat import router as chat_router
from app.v1.vacancies import router as vacancies_router
from app.v1.auth import router as auth_router
import asyncio
from app.services.chat.telegram import main as telegram_main
import uvicorn
import os


app = FastAPI()

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
app.include_router(auth_router, prefix="/auth")


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
