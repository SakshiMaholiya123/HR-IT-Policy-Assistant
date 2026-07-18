from langchain_cohere import CohereEmbeddings

from config.settings import (
    COHERE_API_KEY,
    EMBEDDING_MODEL,
)

class EmbeddingModel:
    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
        api_key: str = COHERE_API_KEY,
    ):
        self.model_name = model_name
        self.api_key = api_key

    def get_embeddings(self) -> CohereEmbeddings:

        return CohereEmbeddings(
            model=self.model_name,
            cohere_api_key=self.api_key,
        )