import logging

from langchain_cohere import CohereEmbeddings

from config.settings import (
    COHERE_API_KEY,
    EMBEDDING_MODEL,
)

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """
    Initializes and provides the embedding model used
    for generating vector embeddings.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
        api_key: str = COHERE_API_KEY,
    ):
        """
        Initialize the embedding model configuration.

        Args:
            model_name: Name of the Cohere embedding model.
            api_key: Cohere API key.
        """
        self.model_name = model_name
        self.api_key = api_key

    def get_embeddings(self) -> CohereEmbeddings:
        """
        Creates and returns a Cohere embedding model.

        Returns:
            CohereEmbeddings: Initialized embedding model.

        Raises:
            ValueError: If the Cohere API key is missing.
        """

        if not self.api_key:
            logger.error(
                "COHERE_API_KEY is not configured."
            )
            raise ValueError(
                "COHERE_API_KEY is missing. "
                "Please configure it in the .env file."
            )

        logger.info(
            "Initializing Cohere embedding model: %s",
            self.model_name,
        )

        embeddings = CohereEmbeddings(
            model=self.model_name,
            cohere_api_key=self.api_key,
        )

        logger.info(
            "Embedding model initialized successfully."
        )

        return embeddings