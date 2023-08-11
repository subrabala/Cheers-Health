from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import UUID4

from sqlalchemy.orm import Session

from typing import List

import models
from database import get_db
import schemas

import uuid

app = FastAPI(prefix='/chatbot')
origins = ['*']

# starting_id = "c8951605-3904-494f-a2a9-ce651dfb211b"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def gen_uuid():
    return uuid.uuid4()


@app.get("/get_question/{question_id}", response_model=schemas.InitialQuestion)
def get_questions(question_id: UUID4, db: Session = Depends(get_db)):
    print(question_id)
    question = db.query(models.Questions).filter(
        models.Questions.id == question_id).first()

    answers = db.query(models.Answers).filter(
        models.Answers.question_id == question_id).all()

    journal_id = gen_uuid()

    response = {"journal_id": journal_id,
                "question": question, "answer_options": answers}

    return response


@app.post("/get_question", response_model=schemas.QuestionAnswers)
def gen_response(payLoad: schemas.GetAnswer, db: Session = Depends(get_db)):
    recieved_answer = db.query(models.Answers).filter(
        models.Answers.id == payLoad.answer_id).first()
    elder_question_expression = db.query(models.Questions).filter(
        models.Questions.id == recieved_answer.question_id).first().expression

    if recieved_answer.progeny_question_id is None:
        response = {"journal_id": payLoad.journal_id, "user_id": payLoad.user_id,
                    "question": None, "answer_options": None}

        journal = models.Journal(
            journal_id=payLoad.journal_id, user_id=payLoad.user_id, score=recieved_answer.score,
            question_id=recieved_answer.question_id, progeny_question_id=None, answer_id=payLoad.answer_id,
            question_expression=elder_question_expression, answer_expression=recieved_answer.expression, suggested_action=recieved_answer.suggested_action
        )

    else:
        question = db.query(models.Questions).filter(
            models.Questions.id == recieved_answer.progeny_question_id).first()
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Progeny Question ID")

        answers = db.query(models.Answers).filter(
            models.Answers.question_id == recieved_answer.progeny_question_id).all()

        response = {"journal_id": payLoad.journal_id, "user_id": payLoad.user_id,
                    "question": question, "answer_options": answers}

        journal = models.Journal(
            journal_id=payLoad.journal_id, user_id=payLoad.user_id, score=recieved_answer.score,
            question_id=recieved_answer.question_id, progeny_question_id=recieved_answer.progeny_question_id, answer_id=payLoad.answer_id,
            question_expression=elder_question_expression, answer_expression=recieved_answer.expression, suggested_action=recieved_answer.suggested_action
        )

    db.add(journal)
    db.commit()
    db.refresh(journal)

    return response
