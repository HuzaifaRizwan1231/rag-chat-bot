from langchain_core.messages import HumanMessage
from utils.response_builder import ResponseBuilder
from utils.pycrypto import encrypt
from utils.langchain import GeminiDocumentRAG, GeminiDocumentCRAG
from utils.langchain import initializeAppWorkflow

app = None
doc_rags = {}
doc_crags = {}


def getLangchainResponse(langchainModel, text, chatId):
    global app
    try:
        # Initialize the workflow
        if app is None:
            app = initializeAppWorkflow(langchainModel)

        # Generating persistent response
        input_messages = [HumanMessage(text)]
        config = {"configurable": {"thread_id": str(chatId)}}
        response = app.invoke({"messages": input_messages}, config)

        # returning the response
        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Response Generated Successfully")
            .setData(encrypt(response["messages"][-1].content))
            .setStatusCode(200)
            .build()
        )

    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occured")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response


def createLangchainRAGInstance(chatId, file_path):
    try:
        global doc_rags, doc_crags

        # Create RAG instance per chatId
        doc_rag = GeminiDocumentRAG(model="gemini-2.5-flash")
        doc_rag.load_document(file_path)
        doc_rags[chatId] = doc_rag

        # Create CRAG Instance
        doc_crag = GeminiDocumentCRAG(model="gemini-2.5-flash")
        doc_crag.load_document(file_path)
        doc_crags[chatId] = doc_crag

        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Document Processed Successfully")
            .setStatusCode(200)
            .build()
        )

    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occured while creating RAG instance")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response


def getLangchainRAGResponse(model, text, chatId):
    try:
        global doc_rags, doc_crags
        answer = ""

        if model == "gemini-rag" and chatId in doc_rags:
            answer = doc_rags[chatId].get_answer(text, chatId)

        elif model == "gemini-crag" and chatId in doc_crags:
            answer = doc_crags[chatId].get_answer(text)

        else:
            answer = "No document found for this chat. Please upload a document first."

        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Response from uploaded document")
            .setData(encrypt(answer))
            .setStatusCode(200)
            .build()
        )

    except Exception as e:
        response = (
            ResponseBuilder()
            .setSuccess(False)
            .setMessage("An Error Occurred while fetching RAG response")
            .setError(str(e))
            .setStatusCode(500)
            .build()
        )
        # Logging the error
        print(response)
        return response
