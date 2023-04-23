from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, UUID
from sqlalchemy.orm import relationship
from english_teacher.adapters.persistence.postgres.sqlalchemy_question import Base


class SqlAlchemyQuestionEmbedding(Base):
    __tablename__ = "question_embeddings"
    __table_args__ = {"schema": "my_schema"}

    question_id = Column(
        UUID(as_uuid=True), ForeignKey("my_schema.questions.id"), primary_key=True
    )
    faiss_id = Column(Integer, nullable=False, index=True)
    embedding = Column(ARRAY(Float), nullable=False)
    model = Column(String)
    prompt_tokens = Column(Integer)
    total_tokens = Column(Integer)

    question = relationship(
        "SqlAlchemyQuestion",
        back_populates="embedding",
        uselist=False,
        cascade="all, delete",
        single_parent=True,
    )
