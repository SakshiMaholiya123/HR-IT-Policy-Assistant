from datetime import date

from pydantic import BaseModel, Field


class LeaveCalculationInput(BaseModel):
    """
    Input for leave balance calculation.
    """

    joining_date: date = Field(
        ...,
        description="Employee's joining date.",
    )

    reference_date: date = Field(
        ...,
        description="Date up to which leave is calculated.",
    )

    accrual_rate: float = Field(
        ...,
        gt=0,
        description="Leave accrued per completed month.",
        examples=[1.5],
    )


class LeaveCalculationOutput(BaseModel):
    """
    Result of leave balance calculation.
    """

    completed_months: int = Field(
        ...,
        ge=0,
        description="Completed months of service.",
    )

    leave_balance: float = Field(
        ...,
        ge=0,
        description="Calculated leave balance.",
    )


class NoticeCalculationInput(BaseModel):
    """
    Input for notice period calculation.
    """

    completed_months: int = Field(
        ...,
        ge=0,
        description="Completed months of service.",
    )

    minimum_months: int = Field(
        ...,
        ge=0,
        description="Minimum months required for higher notice period.",
    )

    lower_notice_days: int = Field(
        ...,
        ge=0,
        description="Notice period before reaching the threshold.",
    )

    higher_notice_days: int = Field(
        ...,
        ge=0,
        description="Notice period after reaching the threshold.",
    )


class NoticeCalculationOutput(BaseModel):
    """
    Result of notice period calculation.
    """

    notice_period_days: int = Field(
        ...,
        ge=0,
        description="Applicable notice period in days.",
    )