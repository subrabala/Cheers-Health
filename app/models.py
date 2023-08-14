from sqlalchemy import Column, Integer, String, Text, VARCHAR, ARRAY, Uuid
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
import uuid


class Questions(Base):
    __tablename__ = "core_questiondataset"

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    id = Column(Uuid(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4())
    expression = Column(Text, nullable=False)
    keyword_intents = Column(VARCHAR[255], nullable=True)


class Answers(Base):
    __tablename__ = "core_answerdataset"

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    id = Column(Uuid(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4())
    expression = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    keyword_intents = Column(ARRAY(String), nullable=True)
    suggested_action = Column(VARCHAR[255], nullable=True)
    elder_question_id = Column(Uuid, nullable=True)
    progeny_question_id = Column(Uuid, nullable=True)
    question_id = Column(Uuid, nullable=False)


class Journal(Base):
    __tablename__ = "journal"
    answered_at = Column(TIMESTAMP(timezone=True), primary_key=True,
                         nullable=False, server_default=text('now()'))
    journal_id = Column(Uuid(as_uuid=True), nullable=False)
    user_id = Column(Uuid(as_uuid=True), nullable=False)
    score = Column(Integer, nullable=False)
    question_id = Column(Uuid, nullable=False)
    progeny_question_id = Column(Uuid, nullable=True)
    answer_id = Column(Uuid(as_uuid=True), nullable=False)
    question_expression = Column(Text, nullable=False)
    answer_expression = Column(Text, nullable=False)
    suggested_action = Column(VARCHAR(255), nullable=True)


class GPTLogs(Base):
    __tablename__ = "gpt_logs"
    asked_at = Column(TIMESTAMP(timezone=True), primary_key=True,
                      nullable=False, server_default=text('now()'))
    user_id = Column(Uuid(as_uuid=True), nullable=False)
    chat_session_id = Column(Uuid(as_uuid=True), nullable=False)
    message_id = Column(Uuid(as_uuid=True), primary_key=True,
                        nullable=False, default=uuid.uuid4())
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)


class PrimaryQuestions(Base):
    __tablename__ = "primary_questions"
    added_at = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text('now()'))
    question_id = Column(Uuid(as_uuid=True), primary_key=True,
                         nullable=False, default=uuid.uuid4())
