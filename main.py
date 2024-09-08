from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables, delete_tables
from router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print('Database is ready')
    yield
    await delete_tables()
    print('Database has been cleared')


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def home():
    return 'Hello, World!'


app.include_router(tasks_router)
