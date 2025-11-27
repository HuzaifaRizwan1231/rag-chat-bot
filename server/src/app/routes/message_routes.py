from fastapi import APIRouter, Request
from dotenv import load_dotenv
from utils.limiter import limiter
from services.database_service import getAllMessagesOfChat, insertMessage
from schemas.message_schema import createMessageRequestSchema

router = APIRouter()
load_dotenv()

@router.get("/get")
def fetchChats(request: Request, chatId: int):
    return getAllMessagesOfChat(chatId)

@router.post("/create")
def createNewMessage(request: Request, message: createMessageRequestSchema):
    return insertMessage(message)