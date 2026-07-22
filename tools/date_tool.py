import logging
from datetime import date

from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class DateTool:
    """
    Provides the current system date.

    This tool is used whenever the agent needs today's
    date for policy-based calculations.
    """

    @staticmethod
    def today() -> str:
        """
        Returns today's date in ISO format (YYYY-MM-DD).

        Returns:
            str: Current system date.
        """

        current_date = date.today().isoformat()

        logger.info(
            "Current date requested: %s",
            current_date,
        )

        return current_date