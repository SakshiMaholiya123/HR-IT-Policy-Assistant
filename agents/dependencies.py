import logging
from dataclasses import dataclass

from config.logging_config import setup_logging
from tools.calculator_tool import LeaveNoticeCalculator
from tools.date_tool import DateTool
from tools.retriever_tool import PolicyRetrieverTool


setup_logging()

logger = logging.getLogger(__name__)


@dataclass
class AgentDependencies:
    """
    Shared dependencies used by the PydanticAI agent.
    """

    retriever: PolicyRetrieverTool
    calculator: LeaveNoticeCalculator
    date_tool: DateTool


def get_dependencies() -> AgentDependencies:
    """
    Creates all shared dependencies required by the agent.

    Returns:
        AgentDependencies
    """

    logger.info("Initializing agent dependencies.")

    dependencies = AgentDependencies(
        retriever=PolicyRetrieverTool(),
        calculator=LeaveNoticeCalculator(),
        date_tool=DateTool(),
    )   

    logger.info("Agent dependencies initialized successfully.")

    return dependencies