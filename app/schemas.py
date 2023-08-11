from pydantic import BaseModel, UUID4
from uuid import uuid4
from sqlalchemy import Column, String
import uuid
from typing import List, Optional


class GetAnswer(BaseModel):
    answer_id: UUID4
    journal_id: UUID4
    user_id: UUID4


class QuestionResponse(BaseModel):
    id: UUID4
    expression: str
    # keyword_intents: list


class AnswerOptions(BaseModel):
    id: UUID4
    expression: str
    # score: int
    # keyword_intents: List
    suggested_action: Optional[str] = None
    # elder_question_id: UUID4
    # progeny_question_id: Optional[UUID4] = None
    # question_id: UUID4


class InitialAnswerOptions(BaseModel):
    id: UUID4
    expression: str
    # score: int
    # keyword_intents: List
    suggested_action: Optional[str] = None
    # progeny_question_id: Optional[UUID4] = None
    # question_id: UUID4


class InitialQuestion(BaseModel):
    journal_id: UUID4
    question: QuestionResponse
    answer_options: List[InitialAnswerOptions]

    class config:
        orm_mode = True


class QuestionAnswers(BaseModel):
    # journal_id: UUID4
    # user_id: UUID4
    question: Optional[QuestionResponse]
    answer_options: Optional[List[AnswerOptions]]

    class Config:
        orm_mode = True
