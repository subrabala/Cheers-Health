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
        models.Journal.journal_id == journal_id, models.Journal.user_id == user_id).all()
    return journals


@router.get("/get/{user_id}", response_model=List[schemas.UserJournals])
def get_journal_ids(user_id: UUID4, db: Session = Depends(get_db)):
    journal_ids = db.query(models.Journal.answered_at, models.Journal.journal_id).filter(
        models.Journal.user_id == user_id).all()
    print(journal_ids)
    return journal_ids
