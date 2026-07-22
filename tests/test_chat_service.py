import asyncio

from agents.chat_service import chat

from models.request_models import ChatRequest


async def main():
    request = ChatRequest(
        query="How many earned leaves do employees receive?",
        session_id="session_001",
    )

    response = await chat(request)

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(response.answer)

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for source in response.sources:
        print(
            f"{source.document} (Page {source.page})"
        )

    print("\n" + "=" * 80)
    print("TOOLS USED")
    print("=" * 80)

    for tool in response.tools_used:
        print(tool)


if __name__ == "__main__":
    asyncio.run(main())