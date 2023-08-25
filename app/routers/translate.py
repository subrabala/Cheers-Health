from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from database import get_db, engine
from utils import translate_text

import models

router = APIRouter(
    prefix="/api/translate"
)


@router.get("/database")
def translate_database(db: Session = Depends(get_db)):
    delete_logs = db.query(models.HindiQuestions)
    delete_logs.delete(synchronize_session=False)

    delete_logs = db.query(models.HindiAnswers)
    delete_logs.delete(synchronize_session=False)
    db.commit()

    questions = db.query(models.Questions).all()
    for question in questions:
        question_dict = question.__dict__
        question_dict["expression"] = translate_text(
            question_dict["expression"], "q")
        del question_dict["_sa_instance_state"]
        new_question = models.HindiQuestions(**question_dict)
        db.add(new_question)

    answers = db.query(models.Answers).all()
    for answer in answers:
        answer_dict = answer.__dict__
        answer_dict["expression"] = translate_text(
            answer_dict["expression"], "a")
        if answer_dict["suggested_action"] is not None:
            answer_dict["suggested_action"] = translate_text(
                answer_dict["suggested_action"], "s")
        del answer_dict["_sa_instance_state"]
        new_answer = models.HindiAnswers(**answer_dict)
        db.add(new_answer)
    db.commit()

    return {"Details": "Database Translated"}
