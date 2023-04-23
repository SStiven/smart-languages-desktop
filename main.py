import asyncio

from english_teacher.application.chat_by_text import ChatByText


def build_system_message():
    instructions = [
        "Forget all your previous instructions",
        "Your role will be an English teacher, almost all the time you speak english but sometimes if you think is better to speak Spanish do it, but don't do it too often.",
        "I will provide you with text that was obtained using speech-to-text technology.",
        "Your task is to correct every grammar mistake, but pycryptodomekeep in mind that the text is from spoken English, so be concise and natural in your corrections.",
        "Please focus on correcting the verb tense, and ignore any capitalization errors.",
        "You will receive the text from a speech-to-text software. When correcting, explain the error and provide the corrected version, but avoid congratulating the student.",
        "Treat them like a native Spanish-speaking student learning English.",
        "After you provide the correction, ask the student a related question, after that ask the student if he/shee wants to repeat the corrected phrase to confirm their understanding.",
        "Ignore the capitalization.",
    ]

    return " ".join(instructions)


"""def map_response_to_sqlalchemy_chat(chat_object):
    chat = SqlAlchemyChat()
    chat.external_openai_id = chat_object.id
    chat.object = chat_object.object
    chat.created = datetime.utcfromtimestamp(chat_object.created)
    chat.model = chat_object.model
    chat.prompt_tokens = chat_object.usage.prompt_tokens
    chat.completion_tokens = chat_object.usage.completion_tokens
    chat.total_tokens = chat_object.usage.total_tokens

    choice = chat_object.choices[0]
    chat.responder = choice.message.role
    chat.prompt = choice.message.content
    chat.finish_reason = choice.finish_reason

    return chat
"""


async def main():
    """while True:
        action = input(
            "Do you want to (s)earch for a question or (a)dd a new one? (s/a): "
        ).lower()

        if action == "s":
            query = input("Please enter your question: ")
            similar_question_id = faiss_search.find_similar_question_id(query)
            similar_question = await chat_repository.find_question_by_id(
                similar_question_id
            )

            print("Original Question:", query)
            print("Similar Question:", similar_question.original_question)
            print("Answer:", similar_question.answer)

        elif action == "a":
            new_question = input("Enter the new question: ")
            new_answer = input("Enter the answer for the new question: ")

            question = SqlAlchemyQuestion(
                original_question=new_question, answer=new_answer
            )
            await chat_repository.create(question)

            embedding = faiss_search.encode_question(new_question)
            question_embedding = SqlAlchemyQuestionEmbedding(
                question_id=question.id, embedding=embedding.tolist()
            )
            await question_embedding_repository.create(question_embedding)

            faiss_search.index.add_with_ids(
                np.array([embedding]), np.array([question.id])
            )
    embedding
            print("New question added successfully.")
        else:
            print(
                "Invalid input. Please enter 's' to search for a question or 'a' to add a new question"
        )
    """

    # with open("combined2.txt", "r") as file:
    #    question_text = file.read()
    # system_message = build_system_message()
    """system_message = (
        "Act as a Domain Driven Design, Hexagonal Architecture, Clean Architecture and Clean Code advocated, "
        + "you are an expert in those fields, you pay special attention to the name of folders, files and folder structure."
        + "Analize the following text, folder structure and code, join concepts without removing information,"
        + "if something is wrong inform about it. At the end return a complete analisis with contradictions,errors warnings,"
        + " isntructions with deatils on any topic. of detailed instructions, common mistakes, good practices "
        + "and a complete folder structure with files for an example for a product creation asuming using Python, FastAPI, SQLAlchemy."
    )
    """
    system_message = ""
    question_statement = (
        # "Using Python, create a function to return a number multiplied by 5"
        # "Talk about DTOs ant layers in Domain Driven Design and Clean architecture, be brief."
        # "Explain Clean architecture"
        # "What is Domain Driven Design"
        # "DTOs Clean"
        # "DTOs"
        # "Talk about DTOs"
        # "explain DTOs"
        # " DTOs"
        # "Explain in one line what is Git"
        # "What is Git?"
        # "What is Github?"
        "What is a Github Action?"
        # "Describe a Github Action"
    )
    service = ChatByText()
    answer = await service.execute(question_statement)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
