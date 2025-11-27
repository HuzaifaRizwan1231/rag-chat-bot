from pydantic import BaseModel
from typing import Optional


class chatCompletionRequestSchema(BaseModel):
    model: str
    text: str


class langchainCompletionRequestSchema(BaseModel):
    model: str
    text: str
    chatId: Optional[int] = None


class updateChatRequestSchema(BaseModel):
    chatId: int
    title: str
