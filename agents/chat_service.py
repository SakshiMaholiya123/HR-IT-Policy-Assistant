import logging

from agents.dependencies import get_dependencies
from agents.memory import ConversationMemory
from agents.policy_agent import policy_agent

from config.logging_config import setup_logging

from models.request_models import ChatRequest
from models.response_models import (
    ChatResponse,
    Source,
)

setup_logging()

logger = logging.getLogger(__name__)

logger.info(
    "Initializing Chat Service..."
)

memory_store: dict[
    str,
    ConversationMemory,
] = {}


async def chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    Processes a user query using the HR & IT Policy Agent.

    Steps:
    1. Retrieve or create the user's conversation memory.
    2. Create the shared dependencies.
    3. Execute the Policy Agent using the stored conversation history.
    4. Build source citations from the retrieved policy chunks.
    5. Save the new conversation messages.
    6. Return the structured response.
    """

    logger.info(
        "Received query for session '%s'.",
        request.session_id,
    )

    memory = memory_store.setdefault(
        request.session_id,
        ConversationMemory(),
    )

    dependencies = get_dependencies()

    logger.info(
        "Running Policy Agent..."
    )

    result = await policy_agent.run(
        user_prompt=request.query,
        deps=dependencies,
        message_history=memory.get_messages(),
    )
    print("\nRetrieved Chunks:")
    print(len(dependencies.retriever.last_retrieved_chunks))

    for chunk in dependencies.retriever.last_retrieved_chunks:
        print(chunk.source, chunk.page)

    memory.add_messages(
        result.new_messages(),
    )

    # CHANGED: policy_agent now returns a plain string (output_type=str),
    # so we build the ChatResponse ourselves instead of casting result.output.
    response = ChatResponse(answer=result.output)

    # ------------------------------------------
    # Populate source citations automatically
    # ------------------------------------------

    sources = []
    seen = set()

    for chunk in dependencies.retriever.last_retrieved_chunks:

        key = (
            chunk.source,
            chunk.page,
        )

        if key not in seen:

            seen.add(key)

            sources.append(
                Source(
                    document=chunk.source,
                    page=chunk.page,
                )
            )

    response.sources = sources
    tools_used = []

    if dependencies.retriever.last_retrieved_chunks:
        tools_used.append("Policy Retriever Tool")

    response.tools_used = tools_used

    logger.info(
        "Added %d source citation(s).",
        len(response.sources),
    )

    logger.info(
        "Successfully processed query for session '%s'.",
        request.session_id,
    )

    return response