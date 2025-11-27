from langchain_core.messages import HumanMessage
from utils.response_builder import ResponseBuilder
from utils.pycrypto import encrypt
from utils.langchain import initializeAppWorkflow, MergestackLangchainAssistant

app = None


def getLangchainResponse(langchainModel, text, modelName, chatId):
    global app, currentModelName
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


def getLangchainResponseMergestack(modelName, text):
    try:

        mergestackAssistant = MergestackLangchainAssistant(modelName)

        response = mergestackAssistant.getResponse(text)
        print(response)
        # returning the response
        return (
            ResponseBuilder()
            .setSuccess(True)
            .setMessage("Response Generated Successfully")
            .setData(encrypt(response))
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
