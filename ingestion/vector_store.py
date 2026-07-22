import logging
from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from config.settings import CHROMA_DB_PATH

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Handles creation and loading of the Chroma
    vector database.
    """

    def __init__(
        self,
        persist_directory: str = str(CHROMA_DB_PATH),
    ):
        """
        Initializes the vector store.

        Args:
            persist_directory:
                Directory where Chroma stores vectors.
        """
        self.persist_directory = persist_directory

    def create_vector_store(
        self,
        documents: List[Document],
        embedding_model: Embeddings,
    ) -> Chroma:
        """
        Creates and persists the Chroma vector store.

        Args:
            documents:
                Chunked documents.

            embedding_model:
                Initialized embedding model.

        Returns:
            Chroma vector store.
        """

        if not documents:
            logger.error(
                "Cannot create vector store. "
                "No documents were provided."
            )
            raise ValueError(
                "Document list cannot be empty."
            )

        logger.info(
            "Creating Chroma vector store with %d chunks.",
            len(documents),
        )

        try:

            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=embedding_model,
                persist_directory=self.persist_directory,
            )

            logger.info(
                "Vector store created successfully."
            )

            logger.info(
                "Persisted at: %s",
                self.persist_directory,
            )

            return vector_store

        except Exception as e:
            logger.exception(
                "Failed to create vector store: %s",
                e,
            )
            raise

    def load_vector_store(
        self,
        embedding_model: Embeddings,
    ) -> Chroma:
        """
        Loads an existing Chroma vector store.

        Args:
            embedding_model:
                Initialized embedding model.

        Returns:
            Chroma vector store.
        """

        if not Path(self.persist_directory).exists():

            logger.error(
                "Vector database not found at %s",
                self.persist_directory,
            )

            raise FileNotFoundError(
                f"Vector database not found at "
                f"{self.persist_directory}"
            )

        logger.info(
            "Loading vector store from %s",
            self.persist_directory,
        )

        try:

            vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=embedding_model,
            )

            logger.info(
                "Vector store loaded successfully."
            )

            return vector_store

        except Exception as e:
            logger.exception(
                "Failed to load vector store: %s",
                e,
            )
            raise