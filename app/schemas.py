from pydantic import BaseModel, UUID4
from uuid import uuid4
import uuid
from typing import List, Optional, Union


def gen_session_id():
    return uuid.uuid4()


class GetQuestion(BaseModel):
    id: UUID4
    session_id: Optional[UUID4] = None


class GetAnswer(GetQuestion):
    pass


class QuestionResponse(BaseModel):
    id: UUID4
    expression: str
    keyword_intents: list


class AnswerOptions(BaseModel):
    id: UUID4
    expression: str
    score: int
    keyword_intents: List
    suggested_actions: Optional[str] = None
    elder_question_id: UUID4
    progeny_question_id: Optional[UUID4] = None
    question_id: UUID4


class QuestionAnswers(BaseModel):
    session_id: UUID4
    question: QuestionResponse
    answer_options: List[AnswerOptions]

    class Config:
        orm_mode = True
