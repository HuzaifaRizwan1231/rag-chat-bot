from fastapi import APIRouter, UploadFile, File, Form, Request
from dotenv import load_dotenv
import google.generativeai as genai
from config.config import (
    GEMINI_API_KEY,
    ALLOWED_GEMINI_MODELS,
)
from schemas.chat_schema import (
    langchainCompletionRequestSchema,
    updateChatRequestSchema,
)
from services.langchain_service import (
    getLangchainResponse,
    createLangchainRAGInstance,
    getLangchainRAGResponse,
)
from services.database_service import (
    insertChat,
    getAllChats,
    deleteChatRecord,
    updateChatRecord,
)
from utils.response_builder import ResponseBuilder
from utils.pycrypto import decrypt, encrypt
from utils.limiter import limiter
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Initialize
router = APIRouter()
load_dotenv()

# API Keys
genai.configure(api_key=GEMINI_API_KEY)
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY


@router.post("/langchain-completion")
@limiter.limit("50/minute")
async def langchainChatCompletion(
    request: Request, body: langchainCompletionRequestSchema
):

    text = body.text
    model = body.model
    chatId = body.chatId

    if model not in ALLOWED_GEMINI_MODELS:
        return (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("Invalid model")
            .setStatusCode(400)
            .build()
        )

    # Decrypt the incoming text
    text = decrypt(text)

    if model in ["gemini-rag", "gemini-crag"]:
        return getLangchainRAGResponse(model, text, chatId)

    # Generic Langchain response
    langchainModel = ChatGoogleGenerativeAI(model=model, api_key=GEMINI_API_KEY)
    return getLangchainResponse(langchainModel, text, chatId)


@router.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...), chatId: int = Form(...)):
    # Save the uploaded file
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
    )
    os.makedirs(base_dir, exist_ok=True)
    file_path = os.path.join(base_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return createLangchainRAGInstance(chatId, file_path)


@router.post("/create")
def createNewChat(request: Request):
    return insertChat()


@router.get("/get")
def fetchChats(request: Request):
    return getAllChats()


@router.delete("/delete")
def deleteChat(request: Request, chatId: int):
    return deleteChatRecord(chatId)


@router.post("/update")
def updateChat(request: Request, body: updateChatRequestSchema):
    return updateChatRecord(body)
