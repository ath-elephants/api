from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from database import Session, new_session
from model import get_rag_answer


class SessionRepository:
    @classmethod
    async def get_last_session(cls, session_id: str) -> Session | None:
        async with new_session() as session:
            query = (
                select(Session)
                .where(Session.session_id == session_id)
                .order_by(Session.timestamp.desc())
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_session(cls, session_id: str, question_count: int):
        async with new_session() as session:
            new_db_session = Session(
                session_id=session_id,
                question_count=question_count,
            )
            session.add(new_db_session)

            await session.flush()
            await session.commit()

    @classmethod
    def is_new_session(cls, last_timestamp: datetime) -> bool:
        time_diff = datetime.now() - last_timestamp
        return time_diff > timedelta(minutes=30)

    @classmethod
    async def update_question_count(cls, session_id: str) -> int:
        async with new_session() as _:
            last_session = await cls.get_last_session(session_id)

            if not last_session or cls.is_new_session(last_session.timestamp):
                await cls.add_session(session_id, 1)
                return 1

            new_question_count = last_session.question_count % 2 + 1
            await cls.add_session(session_id, new_question_count)
            return new_question_count


class HistoryMessage(BaseModel):
    role: str  # in ('user', 'assistant')
    content: str


class History(BaseModel):
    session_id: str
    history: list[HistoryMessage]


router = APIRouter(
    prefix='/api/v1',
    tags=['Answers'],
)


@router.post('/get_answer/')
async def get_answer(query: History):
    session_id = query.session_id
    _ = await SessionRepository.update_question_count(session_id)

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
