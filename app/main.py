from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import UUID4

from sqlalchemy.orm import Session

from typing import List

import models
from database import get_db, engine
from utils import gen_uuid, translate_text
import schemas
import openai

app = FastAPI(prefix='/chatbot')
origins = ['*']

models.Base.metadata.create_all(bind=engine)

# starting_id = "c8951605-3904-494f-a2a9-ce651dfb211b"
pre_prompt = "You are an AI Health Chatbot. The chatbot is helpful, creative, clever, and very friendly."

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/primary_questions", response_model=schemas.GetPrimaryQuestions)
def get_primary(db: Session = Depends(get_db)):
    primary_questions = db.query(models.PrimaryQuestions.question_id).all()
    question_id_list = []
    for question in primary_questions:
        question_id_list.append(question.question_id)

    return {"question_ids":question_id_list}

@app.put("/primary_questions", status_code=status.HTTP_202_ACCEPTED)
def set_primary(payLoad: schemas.SetPrimaryQuestions, db: Session = Depends(get_db)):
    existing_questions = db.query(models.PrimaryQuestions).delete()
    db.commit()

    new_primary_questions = []
    for question in payLoad.question_ids:
        new_primary_questions.append(
            models.PrimaryQuestions(question_id=question))
    db.add_all(new_primary_questions)
    db.commit()

    return {"Details": "Questions Updated"}

@app.get("/get_question/{language}/{question_id}", response_model=schemas.InitialQuestion)
def get_questions(question_id: UUID4, language: str, db: Session = Depends(get_db)):
    if language=="en":
        question = db.query(models.Questions).filter(
            models.Questions.id == question_id).first()

        answers = db.query(models.Answers).filter(
            models.Answers.question_id == question_id).all()

        journal_id = gen_uuid()

        response = {"journal_id": journal_id,
                    "question": question, "answer_options": answers}

        return response
    elif language == "hi":
        question = db.query(models.HindiQuestions).filter(
            models.HindiQuestions.id == question_id).first()

        answers = db.query(models.HindiAnswers).filter(
            models.HindiAnswers.question_id == question_id).all()

        journal_id = gen_uuid()

        response = {"journal_id": journal_id,
                    "question": question, "answer_options": answers}

        return response
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Language Not Supported")


@app.post("/get_question/{language}", response_model=schemas.QuestionAnswers)
def gen_response(language: str, payLoad: schemas.GetAnswer, db: Session = Depends(get_db)):
    if language == "en":
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

    if language == "hi":
        recieved_answer = db.query(models.HindiAnswers).filter(
            models.HindiAnswers.id == payLoad.answer_id).first()
        elder_question_expression = db.query(models.HindiQuestions).filter(
            models.HindiQuestions.id == recieved_answer.question_id).first().expression

        if recieved_answer.progeny_question_id is None:
            response = {"journal_id": payLoad.journal_id, "user_id": payLoad.user_id,
                        "question": None, "answer_options": None}

            journal = models.Journal(
                journal_id=payLoad.journal_id, user_id=payLoad.user_id, score=recieved_answer.score,
                question_id=recieved_answer.question_id, progeny_question_id=None, answer_id=payLoad.answer_id,
                question_expression=elder_question_expression, answer_expression=recieved_answer.expression, suggested_action=recieved_answer.suggested_action
            )

        else:
            question = db.query(models.HindiQuestions).filter(
                models.HindiQuestions.id == recieved_answer.progeny_question_id).first()
            if question is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Progeny Question ID")

            answers = db.query(models.HindiAnswers).filter(
                models.HindiAnswers.question_id == recieved_answer.progeny_question_id).all()

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

@app.get("/translate_database")
def translate_database(db: Session = Depends(get_db)):
    questions = db.query(models.Questions).all()
    for question in questions:
        question.expression = translate_text(question.expression)
        question = question.__dict__
        del question["_sa_instance_state"]
        print(question["expression"])
        new_question = models.HindiQuestions(**question)
        db.add(new_question)
        db.commit()


    answers = db.query(models.Answers).all()
    for answer in answers:
        answer.expression = translate_text(answer.expression)
        answer.suggested_action = translate_text(answer.suggested_action)
        answer = answer.__dict__
        del answer["_sa_instance_state"]
        print(answer["expression"])
        new_answer = models.HindiAnswers(**answer)
        db.add(new_answer)
        db.commit()


    return {"Details": "Database Translated"}