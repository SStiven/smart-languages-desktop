from english_teacher.adapters.persistence.postgres.sqlalchemy_chat import SqlAlchemyChat
from .postgres_session_factory import session_factory


class ChatRepository:
    def __init__(self):
        self._session_factory = session_factory

    async def create(self, chat: SqlAlchemyChat) -> SqlAlchemyChat:
        async with self._session_factory() as session:
            session.add(chat)
            await session.commit()
            await session.refresh(chat)
        return chat
