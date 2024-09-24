from datetime import datetime, timedelta

from sqlalchemy import select

from database import SessionModel, new_session


class SessionRepository:
    @staticmethod
    async def _get_last_session(session_id: str) -> SessionModel | None:
        async with new_session() as session:
            query = (
                select(SessionModel)
                .where(SessionModel.session_id == session_id)
                .order_by(SessionModel.timestamp.desc())
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    def _is_new_session(last_timestamp: datetime) -> bool:
        time_diff = datetime.now() - last_timestamp
        return time_diff > timedelta(minutes=30)

    @staticmethod
    async def _add_session(session_id: str, question_count: int) -> None:
        async with new_session() as session:
            new_db_session = SessionModel(
                session_id=session_id,
                question_count=question_count,
            )
            session.add(new_db_session)

            await session.flush()
            await session.commit()

    @classmethod
    async def update_question_count(cls, session_id: str) -> int:
        async with new_session() as _:
            last_session = await cls._get_last_session(session_id)

            if not last_session or cls._is_new_session(last_session.timestamp):
                await cls._add_session(session_id, 1)
                return 1

            new_question_count = last_session.question_count % 2 + 1
            await cls._add_session(session_id, new_question_count)
            return new_question_count
