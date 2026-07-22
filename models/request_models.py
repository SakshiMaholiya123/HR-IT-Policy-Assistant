from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request model for incoming chat requests.
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural language question from the user.",
        examples=[
            "How many earned leaves do I get?",
        ],
    )

    session_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique identifier for maintaining conversation history.",
        examples=[
            "user_12345",
        ],
    )