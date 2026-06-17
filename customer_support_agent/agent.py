import logging
from typing import Any

from google.adk import Agent, Event, Workflow
from google.adk.apps import App

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("customer-support-agent")

# 1. Classification Agent
# This agent determines whether the user query is related to shipping or not.
classifier_agent = Agent(
    name="classifier_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a classifier for a shipping company customer support system.
    Analyze the user's query and classify it into one of two categories:
    - SHIPPING_RELATED: If the query is about shipping rates, tracking, delivery,
      returns, package status, transit time, shipping options, pickup, address
      changes, or anything related to shipping packages.
    - UNRELATED: If the query is about general topics, jokes, weather, writing
      code, general knowledge, or anything not related to shipping.

    Output exactly "SHIPPING_RELATED" or "UNRELATED".
    Do not include any other text, reasoning, or markdown formatting.
    """,
    output_schema=str,
)


# 2. Router Function
# Evaluates the output of classifier_agent and determines the next node.
def router(node_input: str) -> Event:
    logger.info("Router received classification: %s", node_input)
    clean_input = node_input.strip().upper()
    if "SHIPPING_RELATED" in clean_input:
        return Event(route="SHIPPING_RELATED")
    return Event(route="UNRELATED")


# 3. Shipping FAQ Agent
# This agent answers shipping-related queries.
shipping_faq_agent = Agent(
    name="shipping_faq_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a helpful customer support representative for a shipping company.
    Answer the user's shipping-related questions (such as rates, tracking,
    delivery, returns, options) politely, accurately, and professionally.
    """,
    output_schema=str,
)


# 4. Decline Node
# A function node that politely declines to answer unrelated queries.
def decline_to_answer(_node_input: Any = None) -> Event:
    polite_response = (
        "I'm sorry, but I can only assist with questions related to shipping "
        "(such as rates, tracking, delivery, and returns). "
        "How can I help you with your shipping needs today?"
    )
    return Event(
        message=polite_response,
        output=polite_response,
    )


# 5. Define the workflow graph and its edges
root_agent = Workflow(
    name="customer_support_workflow",
    edges=[
        ("START", classifier_agent, router),
        (
            router,
            {
                "SHIPPING_RELATED": shipping_faq_agent,
                "UNRELATED": decline_to_answer,
            },
        ),
    ],
)

# 6. Define the App container
app = App(
    name="customer_support_agent",
    root_agent=root_agent,
)
