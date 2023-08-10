from pydantic import BaseModel, UUID4
from uuid import uuid4
from typing import List


class CellPosition(BaseModel):
    cell: str


class InitQuestion(BaseModel):
    id: UUID4
    expression: str
    keyword_intents: list

    class Config:
        orm_mode = True


class QuestionResponse(BaseModel):
    question: str
    options: dict

    class Config:
        orm_mode = True
