import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")


class OpenAIEmbeddingClient:
    def build(self, question: str):
        response = openai.Embedding.create(
            input=question, model="text-embedding-ada-002"
        )
        # return embedding_response.data[0].embedding
        return response
