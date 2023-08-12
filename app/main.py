from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import UUID4

from sqlalchemy.orm import Session

from typing import List

import models
from database import get_db
import schemas
import openai

import uuid

app = FastAPI(prefix='/chatbot')
origins = ['*']

# starting_id = "c8951605-3904-494f-a2a9-ce651dfb211b"
pre_prompt = "You are an AI Health Chatbot. The chatbot is helpful, creative, clever, and very friendly."

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


@app.post("/gpt_response", response_model=schemas.GPTResponse)
def gpt_response(payLoad: schemas.GPTQuery, db: Session = Depends(get_db)):
    if payLoad.chat_session_id is None:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            prompt=[{"role": "system", "content": pre_prompt}, {"role": "user", "content": payLoad.query}],
            stop="bye",
        )
        return {"chat_session_id": gen_uuid(), "response": response.choices[0].message.content.strip()}


    history = db.query(models.GPTLogs).filter(models.GPTLogs.chat_session_id==payLoad.chat_session_id).all()

    chat_history = []

    for chat in history:
        chat_history.append({"role": "user", "content": chat.query})
        chat_history.append({"role": "assistant", "content": chat.response})

    chat_history.append({"role": "user", "content": payLoad.query})

    print(chat_history)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        prompt= chat_history,
        # temperature=0.9,
        # max_tokens=150,
        # frequency_penalty=0,
        # presence_penalty=0.6,
        stop="bye",
    )

    print(response.choices[0].message.role)

    chat_history = []

    new_chat = models.GPTLogs(user_id=payLoad.user_id, chat_session_id=payLoad.chat_session_id,
                              query=payLoad.query, response=response.choices[0].message.content.strip())


    db.add(new_chat)
    db.commit()

    return {"response": response.choices[0].message.content.strip()}
