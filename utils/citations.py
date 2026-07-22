from typing import List

from langchain_core.documents import Document


def format_citation(
    document: Document,
) -> str:
    """
    Formats a citation for a single retrieved document.

    Args:
        document: Retrieved LangChain document.

    Returns:
        Citation string in the format:
        "<document> (Page <page>)"
    """

    source = document.metadata.get(
        "source",
        "Unknown Document",
    )

    page = document.metadata.get(
        "page",
        "Unknown",
    )

    return f"{source} (Page {page})"


def format_multiple_citations(
    documents: List[Document],
) -> List[str]:
    """
    Formats citations for multiple retrieved documents.

    Duplicate citations are removed while preserving order.

    Args:
        documents: List of retrieved documents.

    Returns:
        List of unique citation strings.
    """

    citations = []

    seen = set()

    for document in documents:

        citation = format_citation(document)

        if citation not in seen:
            citations.append(citation)
            seen.add(citation)

    return citations