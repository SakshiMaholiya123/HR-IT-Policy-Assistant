import logging

from config.logging_config import setup_logging


setup_logging()

logger = logging.getLogger(__name__)


def log_retrieval(
    query: str,
    source: str,
    page: int,
    chunk_id: str,
    score: float,
) -> None:
    """
    Logs information about a retrieved policy chunk.
    """

    logger.info(
        (
            "QUERY='%s' | "
            "SOURCE='%s' | "
            "PAGE=%d | "
            "CHUNK='%s' | "
            "SCORE=%.4f"
        ),
        query,
        source,
        page,
        chunk_id,
        score,
    )


def log_tool_invocation(
    tool_name: str,
) -> None:
    """
    Logs the name of the tool invoked by the agent.
    """

    logger.info(
        "TOOL INVOKED: %s",
        tool_name,
    )