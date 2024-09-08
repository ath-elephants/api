from pydantic import BaseModel
from typing import List


class HistoryMessage(BaseModel):
    role: str  # in ('user', 'assistant')
    content: str


class History(BaseModel):
    session_id: str
    history: List[HistoryMessage]
