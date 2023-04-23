from typing import List
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from Crypto.Hash import SHA256

from english_teacher.adapters.persistence.postgres.sqlalchemy_question_embedding import (
    SqlAlchemyQuestionEmbedding,
)

from .sqlalchemy_question import SqlAlchemyQuestion
from .postgres_session_factory import session_factory


class SqlAlchemyQuestionRepository:
    def __init__(self):
        self._session_factory = session_factory

    async def add(self, question: SqlAlchemyQuestion) -> SqlAlchemyQuestion:
        async with self._session_factory() as session:
            question.statement_hash = SHA256.new(question.statement.encode()).digest()
            session.add(question)
            await session.commit()
            await session.refresh(question)
        return question

    async def find_all_by_embedding_indices(
        self, ids: List[int]
    ) -> List[SqlAlchemyQuestion]:
        async with self._session_factory() as session:
            statement = (
                select(SqlAlchemyQuestion)
                .join(SqlAlchemyQuestionEmbedding)
                .where(SqlAlchemyQuestionEmbedding.faiss_id.in_(ids))
                .options(joinedload(SqlAlchemyQuestion.answers))
            )
            result = await session.execute(statement)
            return result.unique().scalars().all()

    async def find_by_statement(self, statement: str) -> SqlAlchemyQuestion:
        async with self._session_factory() as session:
            sha256_hash = SHA256.new(statement.encode()).digest()

            stmt = (
                select(SqlAlchemyQuestion)
                .options(
                    joinedload(SqlAlchemyQuestion.embedding),
                    joinedload(SqlAlchemyQuestion.answers),
                )
                .where(SqlAlchemyQuestion.statement_hash == sha256_hash)
            )
            result = await session.execute(stmt)
            return result.unique().scalar_one_or_none()
