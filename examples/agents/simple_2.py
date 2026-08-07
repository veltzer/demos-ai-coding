#!/usr/bin/env python

"""
Stage 2: loop asking the user for questions and issuing them to anthropic.

Each question is an independent request -- no conversation history is kept, so
follow-up questions do not work yet.

The modules you need to install to make this work are `passpy` and `anthropic`
"""

import passpy
import anthropic

MODEL = "claude-opus-5"

store = passpy.Store()
api_key = store.get_key("keys/claude.ai")
assert api_key is not None
api_key = api_key.rstrip()
client = anthropic.Anthropic(api_key=api_key)

print("Ask me anything. Type 'exit' or 'quit' (or Ctrl-D) to stop.")
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
    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        messages=[{"role": "user", "content": question}],
    )
    for block in response.content:
        if block.type == "text":
            print(block.text)
