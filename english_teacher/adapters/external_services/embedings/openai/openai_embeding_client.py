import openai
import openai

openai.api_key = "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"


class OpenAIEmbeddingClient:
    def build(self, question: str):
        response = openai.Embedding.create(
            input=question, model="text-embedding-ada-002"
        )
        # return embedding_response.data[0].embedding
        return response
