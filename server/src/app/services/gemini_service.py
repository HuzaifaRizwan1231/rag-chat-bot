import google.generativeai as genai
from utils.response_builder import ResponseBuilder
from config.config import MAX_OUTPUT_TOKENS, TEMPERATURE
from utils.pycrypto import encrypt

def geminiChatCompletion(model, text):
    try:     
        model = genai.GenerativeModel(model)
        response = model.generate_content(text, generation_config=genai.GenerationConfig(
            max_output_tokens=MAX_OUTPUT_TOKENS,
            temperature=TEMPERATURE,
        ))
        encrypted_data = encrypt(response.text)
        return ResponseBuilder().setSuccess(True).setMessage("Response Generated Successfully").setData(encrypted_data).setStatusCode(200).build()

    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(e).setStatusCode(500).build()
        print(response)
        return response