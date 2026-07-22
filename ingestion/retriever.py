import logging
from typing import List, Tuple

from langchain_core.documents import Document

from config.settings import TOP_K
from ingestion.embedder import EmbeddingModel
from ingestion.vector_store import VectorStore
from models.response_models import RetrievedChunk   # <-- import your pydantic model
from utils.similarity import passes_grounding_threshold


logger = logging.getLogger(__name__)


class PolicyRetriever:
    """
    Retrieves the most relevant policy chunks
    from the Chroma vector database.
    """

    def __init__(self, top_k: int = TOP_K):
        self.top_k = top_k

        embedding_model = EmbeddingModel().get_embeddings()

        self.vector_store = VectorStore().load_vector_store(
            embedding_model=embedding_model,
        )

        # NEW: track the last set of retrieved chunks
        # so chat_service.py can read it after the agent runs.
        self.last_retrieved_chunks: List[RetrievedChunk] = []

        logger.info("Policy Retriever initialized successfully.")

    def retrieve(self, query: str) -> List[Tuple[Document, float]]:
        """
        (unchanged — your existing low-level retrieval logic)
        """
        logger.info("Retrieving documents for query: %s", query)

        try:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=self.top_k,
            )

            logger.info("Retrieved %d candidate chunks.", len(results))

            filtered_results = []

            for document, score in results:
                source = document.metadata.get("source", "Unknown")

                logger.info("Distance Score: %.4f | Source: %s", score, source)

                passed = passes_grounding_threshold(score)

                logger.info("Score: %.4f | Threshold Passed: %s", score, passed)

                if passed:
                    filtered_results.append((document, score))

            logger.info(
                "%d chunks passed grounding threshold.",
                len(filtered_results),
            )

            return filtered_results

        except Exception as e:
            logger.exception("Failed to retrieve documents: %s", e)
            raise

    def search(self, query: str) -> List[RetrievedChunk]:
        """
        NEW: Public method used by the agent tool.

        Wraps retrieve(), converts (Document, score) tuples into
        RetrievedChunk objects, caches them on self.last_retrieved_chunks
        for chat_service.py to read, and returns them.
        """

        results = self.retrieve(query)

        chunks: List[RetrievedChunk] = []

        for document, score in results:
            chunks.append(
                RetrievedChunk(
                    source=document.metadata.get("source", "Unknown"),
                    page=document.metadata.get("page", 1),
                    chunk_id=document.metadata.get("chunk_id", ""),
                    similarity_score=score,
                    content=document.page_content,
                )
            )

        # cache for chat_service.py
        self.last_retrieved_chunks = chunks

        return chunks