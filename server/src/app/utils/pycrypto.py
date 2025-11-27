from fastapi import HTTPException
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from config.config import AES_SECRET_KEY, AES_IV
from utils.response_builder import ResponseBuilder
import base64
import json

# Retrieving and padding AES Secret Key and IV
AES_SECRET_KEY = bytes.fromhex(AES_SECRET_KEY)
AES_IV = bytes.fromhex(AES_IV)
AES_SECRET_KEY = AES_SECRET_KEY.ljust(16, b'\0')[:16]
AES_IV = AES_IV.ljust(16, b'\0')[:16]

def decrypt(ciphertext: str) -> dict:
    try:
        # Decode the base64-encoded ciphertext
        encrypted_data = base64.b64decode(ciphertext)
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
        # Decrypt and unpad the data
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return json.loads(decrypted.decode('utf-8'))
    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(str(e)).setStatusCode(500).build()
        print(response)
        return response
    
def encrypt(data: dict) -> str:
    try:
        # Convert the data to JSON
        data_json = json.dumps(data)
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
        # Pad the data to be AES block size compliant
        padded_data = pad(data_json.encode('utf-8'), AES.block_size)
        # Encrypt and encode the data in base64
        encrypted_data = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode('utf-8')
    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(str(e)).setStatusCode(500).build()
        print(response)
        return response