from sqlalchemy import Column, String, LargeBinary
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

from english_teacher.adapters.persistence.postgres.sqlalchemy_chat import Base


class SqlAlchemyQuestion(Base):
    __tablename__ = "questions"
    __table_args__ = {"schema": "my_schema"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    statement = Column(String, unique=True)
    statement_hash = Column(LargeBinary, unique=True, index=True)

    embedding = relationship(
        "SqlAlchemyQuestionEmbedding", back_populates="question", uselist=False
    )

    answers = relationship("SqlAlchemyAnswer", back_populates="question")
