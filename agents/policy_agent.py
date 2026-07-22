import logging

from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider

from agents.dependencies import AgentDependencies
from agents.tool_registry import register_tools

from config.logging_config import setup_logging
from config.settings import (
    MISTRAL_API_KEY,
    LLM_MODEL,
)

from prompts.system_prompt import SYSTEM_PROMPT

setup_logging()

logger = logging.getLogger(__name__)

logger.info("Initializing Policy Agent...")

policy_agent = Agent(
    model=MistralModel(
        LLM_MODEL,
        provider=MistralProvider(
            api_key=MISTRAL_API_KEY,
        ),
    ),
    deps_type=AgentDependencies,
    output_type=str,
    system_prompt=SYSTEM_PROMPT,
)

register_tools(policy_agent)

logger.info(
    "Policy Agent initialized successfully."
)