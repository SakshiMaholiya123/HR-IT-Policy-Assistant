from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    """
    Represents a retrieved policy chunk.
    """

    source: str = Field(
        ...,
        description="Source document name.",
    )

    page: int = Field(
        ...,
        ge=1,
        description="Page number.",
    )

    chunk_id: str = Field(
        ...,
        description="Unique chunk identifier.",
    )

    similarity_score: float = Field(
        ...,
        description="Similarity score returned by Chroma.",
    )

    content: str = Field(
        ...,
        description="Retrieved policy text.",
    )