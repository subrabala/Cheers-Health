from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from database import get_db, engine
from utils import gen_uuid
from config import settings

import openai

import models
import schemas

router = APIRouter(
    prefix="/api/gpt_response"
)
openai.api_key = settings.openai_api_key
pre_prompt = "You are an AI Health Chatbot. The chatbot is helpful, creative, clever, and very friendly."

@router.post("/", response_model=schemas.GPTResponse)
def gen_gpt_response(payLoad: schemas.GPTQuery, db: Session = Depends(get_db)):
    if payLoad.chat_session_id is None:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": pre_prompt}, {"role": "user", "content": payLoad.query}],
            stop="bye",
        )
        chat_session_id = gen_uuid()
        new_chat = models.GPTLogs(user_id=payLoad.user_id, chat_session_id=chat_session_id,
                                query=payLoad.query, response=response.choices[0].message.content.strip())

        db.add(new_chat)
        db.commit()
        return {"chat_session_id": chat_session_id, "response": response.choices[0].message.content.strip()}


    history = db.query(models.GPTLogs).filter(models.GPTLogs.chat_session_id==payLoad.chat_session_id).all()

    chat_history = []

    for chat in history:
        chat_history.append({"role": "user", "content": chat.query})
        chat_history.append({"role": "assistant", "content": chat.response})

    chat_history.append({"role": "user", "content": payLoad.query})

    print(chat_history)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = chat_history,
        # temperature=0.9,
        # max_tokens=150,
        # frequency_penalty=0,
        # presence_penalty=0.6,
        stop="bye",
    )

    print(response.choices[0].message.role)

    chat_history = []

    new_chat = models.GPTLogs(user_id=payLoad.usopeer_id, chat_session_id=payLoad.chat_session_id,
                              query=payLoad.query, response=response.choices[0].message.content.strip())


    db.add(new_chat)
    db.commit()

    return {"chat_session_id": payLoad.chat_session_id, "response": response.choices[0].message.content.strip()}
