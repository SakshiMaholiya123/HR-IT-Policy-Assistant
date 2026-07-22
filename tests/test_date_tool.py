from tools.date_tool import DateTool


def main() -> None:
    """
    Manual test for the DateTool.
    """

    print("=" * 50)
    print("Date Tool Test")
    print("=" * 50)

    print(f"Today's Date : {DateTool.today()}")

    print("=" * 50)


if __name__ == "__main__":
    main()