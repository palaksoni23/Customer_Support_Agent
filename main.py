import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add the current directory to path so customer_support_agent package can be imported
sys.path.append(str(Path(__file__).resolve().parent))

# Load environment variables before importing agent modules (API key must be set first)
load_dotenv(dotenv_path=Path("customer_support_agent") / ".env")
load_dotenv()

from google.adk.runners import InMemoryRunner  # noqa: E402

from customer_support_agent.agent import app  # noqa: E402


async def run_query(runner: InMemoryRunner, query: str) -> None:
    print(f"\nQuery: '{query}'")
    print("-" * 50)
    try:
        events = await runner.run_debug(query, quiet=True)

        # Check for message parameter in events (e.g. from the decline node)
        decline_msg = None
        agent_msg = ""

        for event in events:
            # Check for message on the event itself
            if hasattr(event, "message") and event.message:
                decline_msg = event.message

            # Check for content from an LLM Agent
            if hasattr(event, "content") and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        agent_msg += part.text

        if decline_msg:
            print(f"Response (Decline Node): {decline_msg}")
        elif agent_msg:
            print(f"Response (Agent): {agent_msg.strip()}")
        else:
            print("No response text found in events.")
            for idx, event in enumerate(events):
                print(f"Event {idx}: type={type(event).__name__}, attrs={dir(event)}")

    except Exception as e:  # noqa: BLE001
        print(f"Error executing query: {e}")
    print("-" * 50)


async def main() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(
            "WARNING: GOOGLE_API_KEY is not set. "
            "Please set it in 'customer_support_agent/.env' "
            "or export it as an environment variable."
        )
        print("Note: Running LLM calls will fail without a valid API Key.")

    # Initialize the runner
    runner = InMemoryRunner(app=app)

    # Test cases
    test_cases = [
        # Shipping-related queries (Should be routed to shipping FAQ agent)
        "How do I track my package with ID 987654?",
        "What are your rates for standard shipping to New York?",
        "How can I return an item I ordered last week?",
        # Unrelated queries (Should be routed to decline node)
        "What is the capital of Japan?",
        "Can you write a quick Python function to reverse a string?",
    ]

    for query in test_cases:
        await run_query(runner, query)


if __name__ == "__main__":
    asyncio.run(main())
