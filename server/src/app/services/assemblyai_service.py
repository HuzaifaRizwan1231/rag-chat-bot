import assemblyai as aai
from utils.response_builder import ResponseBuilder
from config.config import ASSEMBLYAI_API_KEY
from utils.pycrypto import encrypt

aai.settings.api_key = ASSEMBLYAI_API_KEY

def assemblyaiTranscribe(audioContent):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audioContent)
    encrypted_data = encrypt(transcript.text)
    return ResponseBuilder().setSuccess(True).setMessage("Transcription Generated Successfully").setData(encrypted_data).setStatusCode(200).build()