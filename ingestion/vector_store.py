from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from config.settings import CHROMA_DB_PATH


class VectorStore:
   
    def __init__(
        self,
        persist_directory: str = str(CHROMA_DB_PATH),
    ):
        self.persist_directory = persist_directory

    def create_vector_store(
        self,
        documents: List[Document],
        embedding_model: Embeddings,
    ) -> Chroma:
       
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=self.persist_directory,
        )

        return vector_store

    def load_vector_store(
        self,
        embedding_model: Embeddings,
    ) -> Chroma:
    
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embedding_model,
        )