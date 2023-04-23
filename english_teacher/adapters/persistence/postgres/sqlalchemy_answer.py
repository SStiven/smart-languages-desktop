from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

from english_teacher.adapters.persistence.postgres.sqlalchemy_chat import Base


class SqlAlchemyAnswer(Base):
    __tablename__ = "answers"
    __table_args__ = {"schema": "my_schema"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    statement = Column(String)

    question_id = Column(UUID(as_uuid=True), ForeignKey("my_schema.questions.id"))
    question = relationship("SqlAlchemyQuestion", back_populates="answers")
