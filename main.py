from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine



class InitQ(BaseModel):
    body: str
    name: str | None = None
    surname: str | None = None
    # description: str | None = None


app = FastAPI()


@app.post("/")
async def answer(question: InitQ = Depends()):
    print(question.body)
    if question.body == "1":
        return {"answer": "Hello, 1"}
    else:
        return {"answer": "Hello, something else"}


@app.get("/")
async def home():
    return {"data": "Hello World"}
