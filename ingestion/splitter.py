import logging
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
)

logger = logging.getLogger(__name__)


class DocumentSplitter:
    """
    Splits LangChain documents into smaller chunks while
    preserving metadata.
    """

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

        logger.info(
            "DocumentSplitter initialized "
            "(chunk_size=%d, chunk_overlap=%d)",
            chunk_size,
            chunk_overlap,
        )

    def split_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:
        """
        Splits documents into chunks and enriches each chunk
        with additional metadata.

        Args:
            documents: List of LangChain documents.

        Returns:
            List of chunked documents.
        """

        if not documents:
            logger.warning(
                "No documents provided for splitting."
            )
            return []

        logger.info(
            "Splitting %d documents.",
            len(documents),
        )

        try:
            chunks = self.text_splitter.split_documents(
                documents
            )

            logger.info(
                "Generated %d chunks.",
                len(chunks),
            )

            for index, chunk in enumerate(chunks, start=1):

                chunk.metadata["chunk_id"] = (
                    f"{chunk.metadata['document_id']}"
                    f"_page_{chunk.metadata['page']}"
                    f"_chunk_{index}"
                )

                chunk.metadata["chunk_length"] = (
                    len(chunk.page_content)
                )

            logger.info(
                "Metadata added to all chunks."
            )

            return chunks

        except Exception as e:
            logger.exception(
                "Document splitting failed: %s",
                e,
            )
            raise