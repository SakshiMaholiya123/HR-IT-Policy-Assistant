
import logging
from typing import List

from config.logging_config import setup_logging
from ingestion.retriever import PolicyRetriever
from models.retriever_models import RetrievedChunk

setup_logging()
logger = logging.getLogger(__name__)


class PolicyRetrieverTool:
    """
    Tool for retrieving relevant policy information
    from the vector database.
    """

    def __init__(self):
        self.retriever = PolicyRetriever()

        # Stores the latest retrieval results
        self.last_retrieved_chunks: List[RetrievedChunk] = []

    def search(
        self,
        query: str,
    ) -> List[RetrievedChunk]:
        """
        Retrieves relevant policy chunks.

        Returns:
            List[RetrievedChunk]
        """

        print("\n")
        print("=" * 80)
        print("RETRIEVER TOOL CALLED")
        print("=" * 80)
        print(f"Query: {query}")
        print("=" * 80)
        print("\n")

        logger.info(
            "PolicyRetrieverTool invoked."
        )

        logger.info(
            "Query: %s",
            query,
        )

        results = self.retriever.retrieve(query)

        if not results:
            logger.warning(
                "No documents passed the grounding threshold."
            )
            return []

        logger.info(
            "%d relevant chunk(s) retrieved.",
            len(results),
        )

        retrieved_chunks: List[RetrievedChunk] = []

        for index, (document, score) in enumerate(
            results,
            start=1,
        ):

            logger.info(
                "Chunk %d | %s | Page %d | Score %.4f",
                index,
                document.metadata["source"],
                document.metadata["page"],
                score,
            )

            retrieved_chunks.append(
                RetrievedChunk(
                    source=document.metadata["source"],
                    page=document.metadata["page"],
                    chunk_id=str(document.metadata["chunk_id"]),   # cast to string
                    similarity_score=score,
                    content=document.page_content,
                )
            )
        # Store the retrieved chunks so they can be
        # accessed later by the chat service.
        
        self.last_retrieved_chunks = retrieved_chunks

        return retrieved_chunks