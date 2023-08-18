from fastapi import Depends, status, APIRouter

from sqlalchemy.orm import Session

from database import get_db, engine

import models
import schemas

router = APIRouter(
    prefix="/primary_questions"
)


@router.get("/", response_model=schemas.GetPrimaryQuestions)
def get_primary_questions(db: Session = Depends(get_db)):
    primary_questions = db.query(models.PrimaryQuestions.question_id).all()
    question_id_list = []
    for question in primary_questions:
        question_id_list.append(question.question_id)

    return {"question_ids": question_id_list}


@router.put("/", status_code=status.HTTP_202_ACCEPTED)
def set_primary_questions(payLoad: schemas.SetPrimaryQuestions, db: Session = Depends(get_db)):
    existing_questions = db.query(models.PrimaryQuestions).delete()
    db.commit()

    new_primary_questions = []
    for question in payLoad.question_ids:
        new_primary_questions.append(
            models.PrimaryQuestions(question_id=question))
    db.add_all(new_primary_questions)
    db.commit()

    return {"Details": "Questions Updated"}
