from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
)


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

    def split_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:

        chunks = self.text_splitter.split_documents(documents)

        for index, chunk in enumerate(chunks, start=1):
            chunk.metadata["chunk_id"] = (
                f"{chunk.metadata['document_id']}"
                f"_page_{chunk.metadata['page']}"
                f"_chunk_{index}"
            )
            chunk.metadata["chunk_length"] = len(chunk.page_content)

        return chunks