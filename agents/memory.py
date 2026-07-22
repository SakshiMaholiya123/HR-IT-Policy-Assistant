from pydantic_ai.messages import ModelMessage


class ConversationMemory:
    """
    Stores the conversation history for a user session.
    """

    def __init__(self):
        self.messages: list[ModelMessage] = []

    def add_messages(
        self,
        messages: list[ModelMessage],
    ) -> None:
        """
        Appends new messages generated during an agent run.
        """

        self.messages.extend(messages)

    def get_messages(
        self,
    ) -> list[ModelMessage]:
        """
        Returns the stored conversation history.
        """

        return self.messages

    def clear(
        self,
    ) -> None:
        """
        Clears the conversation history.
        """

        self.messages.clear()