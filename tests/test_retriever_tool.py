from tools.retriever_tool import PolicyRetrieverTool


def main() -> None:
    """
    Manual test for the PolicyRetrieverTool.
    """

    tool = PolicyRetrieverTool()

    query = "How many earned leaves are provided?"

    response = tool.search(query)

    print("=" * 80)
    print("Policy Retriever Tool Test")
    print("=" * 80)

    print(f"Query:\n{query}")

    print("\nRetrieved Response:\n")
    print(response)

    print("=" * 80)


if __name__ == "__main__":
    main()