from tools.calculator_tool import LeaveNoticeCalculator


def main() -> None:
    """
    Test the LeaveNoticeCalculator.
    """

    calculator = LeaveNoticeCalculator()

    try:
        months = calculator.completed_months(
            "2025-01-15",
            "2026-07-20",
        )

        leave = calculator.calculate_leave_balance(
            completed_months=months,
            accrual_rate=1.5,
        )

        notice = calculator.calculate_notice_period(
            completed_months=months,
            minimum_months=24,
            lower_notice_days=30,
            higher_notice_days=60,
        )

        years = calculator.years_of_service(months)

        print("=" * 60)
        print("Leave & Notice Calculator Test")
        print("=" * 60)

        print(f"Completed Months : {months}")
        print(f"Leave Balance    : {leave}")
        print(f"Notice Period    : {notice} days")
        print(f"Years of Service : {years}")

        print("=" * 60)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()