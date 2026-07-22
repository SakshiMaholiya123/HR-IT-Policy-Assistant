from typing import List

from pydantic import BaseModel, Field

from models.response_models import Source


class FinalResponse(BaseModel):
    """
    Final backend response.

    Contains:
    - LLM generated answer
    - retrieved sources
    - tools used
    """

    answer: str = Field(
        ...,
        description="Final assistant answer."
    )

    sources: List[Source] = Field(
        default_factory=list,
        description="Policy documents used."
    )

    tools_used: List[str] = Field(
        default_factory=list,
        description="Tools invoked during execution."
    )