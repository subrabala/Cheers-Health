from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import UUID4

from sqlalchemy.orm import Session

from database import get_db, engine
from utils import gen_uuid, translate_text
from routers import primary, flow, gpt, translate, journal

import openai

import models
import schemas


app = FastAPI(prefix='/chatbot')
origins = ['*']

models.Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(primary.router)
app.include_router(flow.router)
app.include_router(gpt.router)
app.include_router(translate.router)
app.include_router(journal.router)


@app.get("/", status_code=status.HTTP_200_OK)
def hello():
    return {"API Status": "active"}
