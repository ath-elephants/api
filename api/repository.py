from datetime import datetime, timedelta

from sqlalchemy import select

from api.database import Session, new_session


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

            new_question_count = last_session.question_count % 3 + 1
            await cls.add_session(session_id, new_question_count)

            return last_session.question_count
