from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from datetime import datetime
import uuid

Base = declarative_base()


class SqlAlchemyChat(Base):
    __tablename__ = "chat"
    __table_args__ = {"schema": "my_schema"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    external_openai_id = Column(String)
    prompt = Column(String)
    object = Column(String)
    created = Column(DateTime)
    model = Column(String)
    role = Column(String)
    response = Column(String)
    finish_reason = Column(String)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    total_tokens = Column(Integer)
