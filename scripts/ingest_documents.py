import logging

from config.logging_config import setup_logging
from config.settings import PDF_DIRECTORY

from ingestion.loader import PDFLoader
from ingestion.splitter import DocumentSplitter
from ingestion.embedder import EmbeddingModel
from ingestion.vector_store import VectorStore

setup_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting ingestion pipeline.")

    # 1. Load PDFs
    loader = PDFLoader(str(PDF_DIRECTORY))
    documents = loader.load_documents()

    if not documents:
        logger.error("No documents loaded. Aborting ingestion.")
        return

    # 2. Split into chunks
    splitter = DocumentSplitter()
    chunks = splitter.split_documents(documents)

    # 3. Build embeddings
    embedding_model = EmbeddingModel().get_embeddings()

    # 4. Create (and persist) the vector store
    vector_store = VectorStore()
    vector_store.create_vector_store(
        documents=chunks,
        embedding_model=embedding_model,
    )

    logger.info("Ingestion pipeline completed successfully.")


if __name__ == "__main__":
    main()