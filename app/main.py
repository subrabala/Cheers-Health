from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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


def gen_session_id():
    return uuid.uuid4()


@app.get("/get_question", response_model=schemas.QuestionAnswers)
def get_questions(payLoad: schemas.GetQuestion, db: Session = Depends(get_db)):
    if payLoad.session_id is None:
        payLoad.session_id = gen_session_id()
    question = db.query(models.Questions).filter(
        models.Questions.id == payLoad.id).first()
    answers = db.query(models.Answers).filter(
        models.Answers.question_id == payLoad.id).all()
    response = {"session_id": payLoad.session_id,
                "question": question, "answer_options": answers}
    return response


@app.post("/answer", status_code=status.HTTP_200_OK)
def gen_response(payLoad: schemas.GetAnswer):
    return {"ok": "Ok"}
