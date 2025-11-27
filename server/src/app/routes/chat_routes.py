from fastapi import APIRouter, UploadFile, File, Request
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
from services.assemblyai_service import assemblyaiTranscribe
from services.langchain_service import (
    getLangchainResponse,
    getLangchainResponseMergestack,
)
from services.database_service import (
    insertChat,
    getAllChats,
    deleteChatRecord,
    updateChatRecord,
)
from utils.response_builder import ResponseBuilder
from utils.pycrypto import decrypt
from utils.limiter import limiter
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize
router = APIRouter()
load_dotenv()

# API Keys
genai.configure(api_key=GEMINI_API_KEY)


@router.post("/langchain-completion")
@limiter.limit("50/minute")
async def langchainChatCompletion(
    request: Request, body: langchainCompletionRequestSchema
):

    text = body.text
    model = body.model
    chatId = body.chatId

    print(body)

    if model not in ALLOWED_GEMINI_MODELS:
        return (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("Invalid model")
            .setStatusCode(400)
            .build()
        )

    text = decrypt(text)

    langchainModel = ChatGoogleGenerativeAI(model=model, api_key=GEMINI_API_KEY)
    return getLangchainResponse(langchainModel, text, model, chatId)


@router.post("/transcribe")
@limiter.limit("50/minute")
async def transcribe(request: Request, audio: UploadFile = File(...)):
    try:
        # Process the uploaded audio file
        audioContent = await audio.read()
        # Send the audio content as a file
        return assemblyaiTranscribe(audioContent)
    except Exception as e:
        return (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occurred")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )


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
