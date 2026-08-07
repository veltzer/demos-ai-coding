#!/usr/bin/env python

"""
Stage 3: restrict the agent to airline ticket sales, using two calls per turn.

The first call classifies the question as on or off topic; only if it is on
topic does the second call answer it. Stage 4 collapses these into one call.

The modules you need to install to make this work are `passpy` and `anthropic`
"""
# These demos are deliberately flat single-file scripts: the driver code sits
# at module level so the whole agent loop reads top to bottom. That makes a
# helper's parameter shadow the module-level name it is called with.
# pylint: disable=redefined-outer-name


import json

import passpy
import anthropic

MODEL = "claude-opus-5"

CLASSIFIER_SYSTEM = """
You are a topic classifier for an airline ticket sales agent.
Decide whether the user's message is related to airline ticket sales: flight
searches, fares and pricing, booking, changes and cancellations, baggage,
seating, check-in, refunds, loyalty programs, and travel documents for a flight.
Anything else is off topic.
"""

AGENT_SYSTEM = """
You are a helpful airline ticket sales agent. Answer questions about flights,
fares, booking, baggage, seating, and itinerary changes. You have no access to a
live booking system, so be clear about what the customer would need to confirm
with the airline directly.
"""

REFUSAL = "Sorry, I only deal with airline ticket sales."

# A JSON schema makes the classifier's answer machine-readable, so the client
# can branch on a boolean instead of string-matching prose.
CLASSIFIER_SCHEMA = {
    "type": "object",
    "properties": {
        "on_topic": {
            "type": "boolean",
            "description": "True if the message is about airline ticket sales.",
        },
    },
    "required": ["on_topic"],
    "additionalProperties": False,
}


def text_of(response):
    """Concatenate the text blocks of a response, skipping thinking blocks."""
    return "".join(b.text for b in response.content if b.type == "text")


def is_ticket_sales(question):
    """Ask Claude whether the question is about airline ticket sales."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=CLASSIFIER_SYSTEM,
        output_config={
            "effort": "low",
            "format": {"type": "json_schema", "schema": CLASSIFIER_SCHEMA},
        },
        messages=[{"role": "user", "content": question}],
    )
    return json.loads(text_of(response))["on_topic"]


def answer(question):
    """Answer a ticket sales question."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=AGENT_SYSTEM,
        messages=[{"role": "user", "content": question}],
    )
    return text_of(response)


store = passpy.Store()
api_key = store.get_key("keys/claude.ai")
assert api_key is not None
api_key = api_key.rstrip()
client = anthropic.Anthropic(api_key=api_key)

print("Ask me about airline tickets. Type 'exit' or 'quit' (or Ctrl-D) to stop.")
while True:
    try:
        question = input("\n> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break
    if not question:
        continue
    if question.lower() in ("exit", "quit"):
        break
    if is_ticket_sales(question):
        print(answer(question))
    else:
        print(REFUSAL)
