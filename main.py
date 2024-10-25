from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from user_actions.models import TruckDriverCreate, BuisnessOwnerCreate, MainUserData, TransportCompanyOwnerCreate
from user_actions.appLogic import register, Requests, login
from user_actions.jwt_op import verify_token
from chat_actions.appLogic import create_chat, send_message, message_list
from chat_actions.models import Message
from vacancies.appLogic import create_vacancies, apply_vacancy, find_vacancy, all_vacancies, get_applicants
from vacancies.models import VacancyCreate
from typing import List
from settings import origins
from fastapi.templating import Jinja2Templates

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


connectionmanager = ConnectionManager()


@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, decoded_token: dict = Depends(verify_token)):
    # Connect the client
    await connectionmanager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            send_message({"message": data}, chat_id, decoded_token)
            await connectionmanager.send_personal_message(f"You: {data}", websocket)
            await connectionmanager.broadcast(f"Client #{chat_id}: {data}")

    except WebSocketDisconnect:
        connectionmanager.disconnect(websocket)


@app.post("/user/register/truck")
async def user_reg(user: TruckDriverCreate):
    return register(user)


@app.post("/user/register/buisness")
async def buisness_reg(user: BuisnessOwnerCreate):
    return register(user)


@app.post("/user/register/transportcompany")
async def transp_reg(user: TransportCompanyOwnerCreate):
    return register(user)


@app.post("/user/login")
async def login_user(user: MainUserData):
    return login(user)


@app.post("/user/password/reset")
async def reset_password(email: str):
    return Requests(email).password_reset_request()


@app.post("/user/password/{id}")
async def reset_password(id: str, password: str):
    return Requests(id).accept_password(password)


@app.get("/request/{request}")
async def req(request: str):
    return Requests(request).accept_request()


@app.post("/chat/create")
async def cr_chat(second_user: str, decoded_token: dict = Depends(verify_token)):
    return await create_chat([decoded_token["user_id"], second_user])


@app.post("/chat/{chat_id}/messages/send")
async def transfer_message(message: Message, chat_id: str, decoded_token: dict = Depends(verify_token)):
    return send_message(message, chat_id, decoded_token)


@app.post("/chats/{chat_id}/messages")
async def get_messages(chat_id: str, decoded_token: dict = Depends(verify_token)):
    return message_list(chat_id, decoded_token)


@app.post("/vacancie/create")
async def vacancies_create(vacancies: VacancyCreate, decoded_token: dict = Depends(verify_token)):
    return create_vacancies(vacancies, decoded_token)


@app.post("/vacancie/{id}/apply")
async def vacancie_apply(vacancies_id: str, decoded_token: dict = Depends(verify_token)):
    return apply_vacancy(vacancies_id, decoded_token)


@app.get("/vacancie/{id}")
async def get_vacancie(_id: str):
    return find_vacancy(_id)


@app.get("/vacancie")
async def get_vacancies():
    return all_vacancies()


@app.get("/vacancie/{id}/applicants")
async def getapplicants(vacancies_id: str, decoded_token: dict = Depends(verify_token)):
    return get_applicants(vacancies_id, decoded_token)


@app.post("/vacancie/{id}/delete")
async def delete_vacancie(_id: str):
    return delete_vacancie(_id)