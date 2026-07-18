from pathlib import Path
import logging
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class PDFLoader:
  
    def __init__(self, pdf_directory: str):
        self.pdf_directory = Path(pdf_directory)

        if not self.pdf_directory.exists():
            raise FileNotFoundError(
                f"Directory not found: {self.pdf_directory}"
            )

    def load_documents(self) -> List[Document]:
        
        documents: List[Document] = []

        pdf_files = sorted(self.pdf_directory.glob("*.pdf"))

        if not pdf_files:
            logger.warning(
                "No PDF files found in %s",
                self.pdf_directory,
            )
            return documents

        logger.info(
            "Found %d PDF files.",
            len(pdf_files),
        )

        for pdf_file in pdf_files:

            try:
                logger.info(
                    "Loading %s",
                    pdf_file.name,
                )

                loader = PyMuPDFLoader(str(pdf_file))

                docs = loader.load()

                loaded_pages = 0

                for doc in docs:

                    # Skip blank pages
                    if not doc.page_content.strip():
                        continue

                    # Preserve metadata
                    doc.metadata["source"] = pdf_file.name

                    # Convert page number to 1-based indexing
                    doc.metadata["page"] = (
                        doc.metadata.get("page", 0) + 1
                    )

                    # Unique document identifier
                    doc.metadata["document_id"] = pdf_file.stem

                    documents.append(doc)
                    loaded_pages += 1

                logger.info(
                    "Loaded %s (%d pages)",
                    pdf_file.name,
                    loaded_pages,
                )

            except Exception as e:
                logger.error(
                    "Failed to load %s : %s",
                    pdf_file.name,
                    e,
                )

        logger.info(
            "Successfully loaded %d pages from %d PDFs.",
            len(documents),
            len(pdf_files),
        )

        return documents