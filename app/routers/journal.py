from pyexpat import model
from fastapi import Depends, Query, status, HTTPException, APIRouter
from httpx import get
from pydantic import UUID4
from typing import List, Optional, Union
from sqlalchemy import distinct

from sqlalchemy.orm import Session

from database import get_db, engine
from utils import gen_uuid

import models
import schemas

router = APIRouter(
    prefix="/journal"
)


@router.get("/get/{user_id}/{journal_id}", response_model=List[schemas.JournalDetails])
def get_journals(user_id: UUID4, journal_id: UUID4, db: Session = Depends(get_db)):
    journals = db.query(models.Journal).filter(
        models.Journal.journal_id == journal_id, models.Journal.user_id == user_id).order_by(models.Journal.answered_at).all()
    return journals


@router.get("/get/{user_id}", response_model=List[schemas.UserJournals])
def get_journal_ids(user_id: UUID4, db: Session = Depends(get_db)):
    journal_ids = db.query(models.Journal.journal_id).distinct().filter(
        models.Journal.user_id == user_id).all()
    response = []
    for journal_id in journal_ids:
        answered_at = db.query(models.Journal.answered_at).filter(
            models.Journal.journal_id == journal_id[0]).first()
        response.append({"answered_at":answered_at[0], "journal_id":journal_id[0]})
        print(response)
    return response
