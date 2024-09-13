from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.database import create_tables, delete_tables
from api.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await delete_tables()


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def home():
    return 200


app.include_router(router)
