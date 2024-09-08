from fastapi import APIRouter

from utils.repository import SessionRepository
from utils.schemas import History


router = APIRouter(
    prefix='/api/v1',
    tags=['Answers'],
)


@router.post('/get_answer/')
async def get_answer(query: History):
    session_id = query.session_id
    question_number = await SessionRepository.update_question_count(session_id)

    return {'answer': f'{question_number}'}
