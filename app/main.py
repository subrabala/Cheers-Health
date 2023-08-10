from ast import Expression
import pandas as pd

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import models
from database import get_db
import schemas


app = FastAPI(prefix='/chatbot')
origins = ['*']

starting_id = "c8951605-3904-494f-a2a9-ce651dfb211b"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_questions", response_model=schemas.InitQuestion)
def get_questions(db: Session = Depends(get_db)):
    question = db.query(models.Questions).filter(
        models.Questions.id == starting_id).first()
    print(str(question))
    # return {"hello":"hey"}
    return question


@app.post("/gen_response", status_code=status.HTTP_200_OK)
def gen_response(payLoad: schemas.CellPosition):
    return {"ok": "Ok"}
