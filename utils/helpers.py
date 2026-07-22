from datetime import datetime


def clean_text(
    text: str,
) -> str:
    """
    Removes extra whitespace from text.

    Args:
        text: Input text.

    Returns:
        Cleaned text with single spaces.
    """

    if not text:
        return ""

    return " ".join(text.split())


def current_timestamp() -> str:
    """
    Returns the current timestamp.

    Returns:
        Current date and time in
        YYYY-MM-DD HH:MM:SS format.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )