from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from database import create_tables, delete_tables
from router import router


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


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
