from pydantic import BaseModel

class createMessageRequestSchema(BaseModel):
    sender: str
    text: str
    chatId: int
    
