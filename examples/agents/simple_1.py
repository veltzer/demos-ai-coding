#!/usr/bin/env python

"""
Stage 1: issue one hardcoded prompt to anthropic and print the answer.

The modules you need to install to make this work are `passpy` and `anthropic`
"""

import anthropic
import passpy

MODEL = "claude-opus-5"

QUERY = """
What is the capitol of France and how many residents are there?
Make your answer just a string and number with a comma in the middle
"""

store = passpy.Store()
api_key = store.get_key("keys/claude.ai")
assert api_key is not None
api_key = api_key.rstrip()
client = anthropic.Anthropic(api_key=api_key)

response = client.messages.create(
    model=MODEL,
    max_tokens=16000,
    messages=[{"role": "user", "content": QUERY}],
)

# response.content is a list of blocks (thinking, text, ...) -- only the text
# blocks have a .text attribute, so filter rather than indexing [0].
for block in response.content:
    if block.type == "text":
        print(block.text)
