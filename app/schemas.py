from pydantic import BaseModel, UUID4
from uuid import uuid4
from sqlalchemy import Column, String
import uuid
from typing import List, Optional


# REQUEST SCHEMAS


# Request Schema for Getting Answer ID
class GetAnswer(BaseModel):
    answer_id: UUID4
    journal_id: UUID4
    user_id: UUID4

# Request Schema for getting Query for generating GPT Response
class GPTQuery(BaseModel):
    chat_id: UUID4
    user_id: UUID4
    query: str


# RESPONSE SCHEMAS


# Prerequisite Response Schema for Sending Question Expression
class QuestionResponse(BaseModel):
    question_id: UUID4
    expression: str
    # keyword_intents: list

# Prerequisite Response Schema for Sending Answer Expression
class AnswerOptions(BaseModel):
    answer_id: UUID4
    expression: str
    # score: int
    # keyword_intents: List
    suggested_action: Optional[str] = None
    # elder_question_id: UUID4
    # progeny_question_id: Optional[UUID4] = None
    # question_id: UUID4

# Response Schema for Sending Question and Possible Answers based on Answer IDF
class QuestionAnswers(BaseModel):
    # journal_id: UUID4
    # user_id: UUID4
    question: Optional[QuestionResponse]
    answer_options: Optional[List[AnswerOptions]]

    class Config:
        orm_mode = True

# Prerequisite Response Schema for Sending First Answer Expression (Doesn't have Elder Question ID)
class InitialAnswerOptions(BaseModel):
    answer_id: UUID4
    expression: str
    # score: int
    # keyword_intents: List
    suggested_action: Optional[str] = None
    # progeny_question_id: Optional[UUID4] = None
    # question_id: UUID4

# Response Schema for Journal ID and Initial Question
class InitialQuestion(BaseModel):
    journal_id: UUID4
    question: QuestionResponse
    answer_options: List[InitialAnswerOptions]

    class config:
        orm_mode = True
