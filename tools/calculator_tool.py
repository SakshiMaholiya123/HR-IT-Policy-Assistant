import logging
from datetime import date, datetime
from typing import Union

from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class LeaveNoticeCalculator:
    """
    Performs policy-based calculations.

    This tool contains NO company policy.

    All policy values (leave accrual rates,
    notice period thresholds, etc.) must be
    supplied by the agent after retrieving
    them from the policy documents.
    """

    @staticmethod
    def _parse_date(
        input_date: Union[str, date],
    ) -> date:
        """
        Converts a string (YYYY-MM-DD)
        or date object into a date object.
        """

        if isinstance(input_date, date):
            return input_date

        try:
            return datetime.strptime(
                input_date,
                "%Y-%m-%d",
            ).date()

        except ValueError as exc:
            logger.error(
                "Invalid date format: %s",
                input_date,
            )
            raise ValueError(
                "Date must be in YYYY-MM-DD format."
            ) from exc

    @classmethod
    def completed_months(
        cls,
        joining_date: Union[str, date],
        reference_date: Union[str, date],
    ) -> int:
        """
        Calculates completed months of service.
        """

        joining_date = cls._parse_date(joining_date)
        reference_date = cls._parse_date(reference_date)

        months = (
            (reference_date.year - joining_date.year) * 12
            + (reference_date.month - joining_date.month)
        )

        if reference_date.day < joining_date.day:
            months -= 1

        months = max(months, 0)

        logger.info(
            "Completed months calculated: %d",
            months,
        )

        return months

    @staticmethod
    def calculate_leave_balance(
        completed_months: int,
        accrual_rate: float,
    ) -> float:
        """
        Calculates accrued leave.
        """

        if completed_months < 0:
            raise ValueError(
                "Completed months cannot be negative."
            )

        if accrual_rate < 0:
            raise ValueError(
                "Accrual rate cannot be negative."
            )

        leave_balance = completed_months * accrual_rate

        logger.info(
            "Leave balance calculated: %.2f",
            leave_balance,
        )

        return leave_balance

    @staticmethod
    def calculate_notice_period(
        completed_months: int,
        minimum_months: int,
        lower_notice_days: int,
        higher_notice_days: int,
    ) -> int:
        """
        Determines the applicable notice period.
        """

        notice_period = (
            higher_notice_days
            if completed_months >= minimum_months
            else lower_notice_days
        )

        logger.info(
            "Notice period calculated: %d days",
            notice_period,
        )

        return notice_period

    @staticmethod
    def years_of_service(
        completed_months: int,
    ) -> float:
        """
        Converts completed months into years.
        """

        years = round(
            completed_months / 12,
            2,
        )

        logger.info(
            "Years of service: %.2f",
            years,
        )

        return years