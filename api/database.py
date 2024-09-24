from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Model(DeclarativeBase):
    pass


class SessionModel(Model):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
    question_count: Mapped[int] = mapped_column(default=1)


engine = create_async_engine('sqlite+aiosqlite:///sessions.db')
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
