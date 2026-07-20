import logging
from typing import List, Tuple

from langchain_core.documents import Document

from config.settings import TOP_K
from ingestion.embedder import EmbeddingModel
from ingestion.vector_store import VectorStore
from utils.similarity import passes_grounding_threshold

logger = logging.getLogger(__name__)


class PolicyRetriever:
    """
    Retrieves the most relevant policy chunks
    from the Chroma vector database.
    """

    def __init__(
        self,
        top_k: int = TOP_K,
    ):
        self.top_k = top_k

        embedding_model = EmbeddingModel().get_embeddings()

        self.vector_store = VectorStore().load_vector_store(
            embedding_model=embedding_model,
        )

    def retrieve(
        self,
        query: str,
    ) -> List[Tuple[Document, float]]:
        """
        Retrieves the most relevant chunks after applying
        the grounding threshold.

        Args:
            query: User query.

        Returns:
            A list of (Document, similarity_score).
        """

        logger.info(
            "Retrieving documents for query: %s",
            query,
        )

        try:

            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=self.top_k,
            )

            logger.info(
                "Retrieved %d candidate chunks.",
                len(results),
            )

            filtered_results = []

            for document, score in results:

                # Lower score = better match in Chroma
                if passes_grounding_threshold(score):
                    filtered_results.append(
                        (document, score)
                    )

            logger.info(
                "%d chunks passed the grounding threshold.",
                len(filtered_results),
            )

            return filtered_results

        except Exception as e:
            logger.exception(
                "Failed to retrieve documents: %s",
                e,
            )
            raise