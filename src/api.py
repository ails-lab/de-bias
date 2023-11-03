from fastapi import FastAPI
from pydantic import BaseModel


class SimpleRequest(BaseModel):
    language: str
    values: list[str]


class Position(BaseModel):
    start: int
    end: int


class Target(BaseModel):
    language: str
    literal: str
    position: Position


class SimpleResponse(BaseModel):
    body: str
    target: Target


app = FastAPI()


@app.post('/')
async def simple_request(request: SimpleRequest) -> list[SimpleResponse]:
    
    return {'message': 'hello world'}