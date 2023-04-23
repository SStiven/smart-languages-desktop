from english_teacher.adapters.persistence.faiss.faiss_index import FaissIndex
from english_teacher.adapters.persistence.postgres.sqlalchemy_answer import (
    SqlAlchemyAnswer,
)
from english_teacher.adapters.persistence.postgres.sqlalchemy_question import (
    SqlAlchemyQuestion,
)
from english_teacher.adapters.persistence.postgres.sqlalchemy_question_embedding import (
    SqlAlchemyQuestionEmbedding,
)
from english_teacher.adapters.persistence.postgres.sqlalchemy_question_repository import (
    SqlAlchemyQuestionRepository,
)
from english_teacher.adapters.external_services.chat_completion.openai.openai_chat_client import (
    OpenAIChatClient,
)
from english_teacher.adapters.external_services.embedings.openai.openai_embeding_client import (
    OpenAIEmbeddingClient,
)


class ChatByText:
    def __init__(self):
        pass

    async def execute(self, question_statement: str):
        question_repository = SqlAlchemyQuestionRepository()
        question: SqlAlchemyQuestion = await question_repository.find_by_statement(
            question_statement
        )
        if question is not None:
            print(f"Found exactly in the database!!!!\n")
            for ans in question.answers:
                print(ans.statement)
            return

        embedding_client = OpenAIEmbeddingClient()
        embedding_response = embedding_client.build(question_statement)
        embedding = embedding_response.data[0].embedding

        faiss_index = FaissIndex()
        num_embeddings_to_find = 1
        indexes = faiss_index.search(
            embedding, k=num_embeddings_to_find, threshold=0.15
        )
        if len(indexes) > 0:
            print(f"Found {len(indexes)} similar questions:")
            similar_questions = await question_repository.find_all_by_embedding_indices(
                ids=indexes
            )
            for q in similar_questions:
                print(f"question: {q.statement}")
                for a in q.answers:
                    print(f"answer: {a.statement}")
            return

        print("Doesn't found similar questions in faiss index")
        print("Let's spend some money")
        context = ""
        openai_chat_client = OpenAIChatClient(context, model="gpt-3.5-turbo")
        chat_response = openai_chat_client.chat(question_statement)
        answer_statement = chat_response.choices[0].message.content
        print(answer_statement)
        answer = SqlAlchemyAnswer(statement=answer_statement)

        sqlalchemy_question = SqlAlchemyQuestion(statement=question_statement)
        sqlalchemy_question.answers = [answer]
        embedding_client = OpenAIEmbeddingClient()
        embedding_response = embedding_client.build(sqlalchemy_question.statement)
        embedding = embedding_response.data[0].embedding

        faiss_question_id = faiss_index.add(embedding)

        question_embedding = SqlAlchemyQuestionEmbedding(
            embedding=embedding,
            faiss_id=faiss_question_id,
            model=embedding_response.model,
            prompt_tokens=embedding_response.usage.prompt_tokens,
            total_tokens=embedding_response.usage.total_tokens,
            question=sqlalchemy_question,
        )

        sqlalchemy_question.embedding = question_embedding
        sqlalchemy_question = await question_repository.add(sqlalchemy_question)
        return answer_statement
