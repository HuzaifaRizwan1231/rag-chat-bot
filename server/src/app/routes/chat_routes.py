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
from services.assemblyai_service import assemblyaiTranscribe
from services.langchain_service import (
    getLangchainResponse,
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
from utils.langchain import GeminiDocumentRAG

# Initialize
router = APIRouter()
load_dotenv()

doc_rags = {}


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

    # Check if there's a document RAG for this chatId
    if chatId in doc_rags:
        doc_rag = doc_rags[chatId]
        answer = doc_rag.get_answer(text)
        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Response from uploaded document")
            .setData(encrypt(answer))
            .build()
        )

    # Generic Langchain response
    langchainModel = ChatGoogleGenerativeAI(model=model, api_key=GEMINI_API_KEY)
    return getLangchainResponse(langchainModel, text, model, chatId)


@router.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...), chatId: int = Form(...)):
    try:
        # Save the uploaded file
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
        )
        os.makedirs(base_dir, exist_ok=True)
        file_path = os.path.join(base_dir, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Create RAG instance per chatId
        doc_rag = GeminiDocumentRAG(model="gemini-2.5-flash")
        doc_rag.load_document(file_path)
        doc_rags[chatId] = doc_rag

        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Document processed successfully")
            .build()
        )

    except Exception as e:
        return (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("Error")
            .setError(str(e))
            .build()
        )


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
