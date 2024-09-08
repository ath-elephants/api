from sqlalchemy import select
from datetime import datetime, timedelta

from database import Session, new_session


class SessionRepository:
    @classmethod
    async def get_last_session(cls, session_id: str) -> Session | None:
        async with new_session() as session:
            query = (
                select(Session)
                .where(Session.session_id == session_id)
                .order_by(Session.timestamp.desc())
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_session(cls, session_id: str):
        async with new_session() as session:
            new_db_session = Session(session_id=session_id)
            session.add(new_db_session)
            await session.flush()
            await session.commit()

    @classmethod
    def is_new_session(cls, last_timestamp: datetime) -> bool:
        time_diff = datetime.now() - last_timestamp
        return time_diff > timedelta(minutes=30)

    @classmethod
    async def update_question_count(cls, session_id: str) -> int:
        last_session = await cls.get_last_session(session_id)

        if not last_session or cls.is_new_session(last_session.timestamp):
            await cls.add_session(session_id)
            return 1

        new_question_count = last_session.question_count % 3 + 1

        async with new_session() as session:
            last_session.question_count = new_question_count
            last_session.timestamp = datetime.now()
            await session.commit()

        return new_question_count
