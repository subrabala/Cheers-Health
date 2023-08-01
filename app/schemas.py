from pydantic import BaseModel


class CellPosition(BaseModel):
    cell: str


class QuestionResponse(BaseModel):
    question: str
    options: dict

    class Config:
        orm_mode = True
