#!/usr/bin/env python

"""
Stage 4: classify and answer in a single call.

One schema carries both the on/off topic verdict and the answer, so the model
does both jobs in one request. The refusal is printed locally when the model
reports the question is off topic.

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

AGENT_SYSTEM = """
You are a helpful airline ticket sales agent.

For every user message, do two things at once:

1. Decide whether it is related to airline ticket sales: flight searches, fares
   and pricing, booking, changes and cancellations, baggage, seating, check-in,
   refunds, loyalty programs, and travel documents for a flight. Anything else
   is off topic. Report this as `on_topic`.

2. If it is on topic, answer it in `answer`. You have no access to a live
   booking system, so be clear about what the customer would need to confirm
   with the airline directly. If it is off topic, set `answer` to an empty
   string.
"""

REFUSAL = "Sorry, I only deal with airline ticket sales."

REPLY_SCHEMA = {
    "type": "object",
    "properties": {
        "on_topic": {
            "type": "boolean",
            "description": "True if the message is about airline ticket sales.",
        },
        "answer": {
            "type": "string",
            "description": "The answer if on topic, otherwise an empty string.",
        },
    },
    "required": ["on_topic", "answer"],
    "additionalProperties": False,
}


def reply(question):
    """Classify and answer a question in one call; return the text to print."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=AGENT_SYSTEM,
        output_config={"format": {"type": "json_schema", "schema": REPLY_SCHEMA}},
        messages=[{"role": "user", "content": question}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    result = json.loads(text)
    return result["answer"] if result["on_topic"] else REFUSAL


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
    print(reply(question))
