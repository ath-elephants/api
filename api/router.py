from fastapi import APIRouter, HTTPException

from typing import List
from pydantic import BaseModel

from api.model import get_rag_answer
from api.repository import SessionRepository


class HistoryMessage(BaseModel):
    role: str  # in ('user', 'assistant')
    content: str


class History(BaseModel):
    session_id: str
    history: List[HistoryMessage]


router = APIRouter(
    prefix='/api/v1',
    tags=['Answers'],
)


@router.post('/get_answer/')
async def get_answer(query: History):
    session_id = query.session_id
    question_number = await SessionRepository.update_question_count(session_id)

    try:
        user_input = next(
            (msg.content for msg in query.history if msg.role == 'user'), None
        )

        if not user_input:
            raise HTTPException(status_code=400, detail='User message not found')

        answer = get_rag_answer(query.session_id, user_input)

        return {'answer': answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
