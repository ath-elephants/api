from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class STaskAdd(BaseModel):
    name: str
    description: str | None = None


class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


app = FastAPI()


@app.post("/")
async def add_task(task: STaskAdd = Depends()):
    return {"data": task}


@app.get("/")
async def home():
    return {"data": "Hello World"}
