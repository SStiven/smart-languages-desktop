from typing import List
from sqlalchemy import select

from english_teacher.adapters.persistence.postgres.sqlalchemy_question_embedding import (
    SqlAlchemyQuestionEmbedding,
)

from .postgres_session_factory import session_factory


class QuestionEmbeddingRepository:
    def __init__(self):
        self._session_factory = session_factory

    async def create(
        self, question_embedding: SqlAlchemyQuestionEmbedding
    ) -> SqlAlchemyQuestionEmbedding:
        async with self.async_session() as session:
            session.add(question_embedding)
            await session.commit()
            await session.refresh(question_embedding)
        return question_embedding

    async def get_by_id(self, question_id) -> SqlAlchemyQuestionEmbedding:
        async with self.async_session() as session:
            result = await session.execute(
                select(SqlAlchemyQuestionEmbedding).where(
                    SqlAlchemyQuestionEmbedding.question_id == question_id
                )
            )
            return result.scalar_one_or_none()

    async def get_all(self) -> List[SqlAlchemyQuestionEmbedding]:
        async with self.async_session() as session:
            result = await session.execute(select(SqlAlchemyQuestionEmbedding))
            return result.scalars().all()
