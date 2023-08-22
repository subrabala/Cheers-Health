from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware

from database import get_db, engine
from routers import primary, flow, gpt, translate, journal

import models


app = FastAPI(
    title="Cheers Wisdom Chatbot"
)
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(primary.router)
app.include_router(flow.router)
app.include_router(gpt.router)
app.include_router(translate.router)
app.include_router(journal.router)
