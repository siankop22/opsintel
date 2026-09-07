import json

from openai import OpenAI

from app.agents.tools import search_documents
from app.core.config import settings


client = OpenAI(api_key=settings.openai_api_key)


TOOLS = [
    {
        "type": "function",
        "name": "search_documents",
        "description": "Search internal operations documents for evidence.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    }
]


INSTRUCTIONS = """
You are OpsIntel, an enterprise operations investigation agent.

Use available tools to gather evidence before answering.

Give a concise response with:
- Finding
- Evidence
- Likely cause
- Recommended action

Once you have enough evidence, stop searching and provide the final answer.
"""


def investigate(question: str):
    response = client.responses.create(
        model=settings.openai_model,
        instructions=INSTRUCTIONS,
        input=question,
        tools=TOOLS,
    )

    tool_log = []

    for _ in range(5):
        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            return {
                "answer": response.output_text,
                "tool_calls": tool_log,
            }

        tool_outputs = []

        for item in function_calls:
            if item.name == "search_documents":
                arguments = json.loads(item.arguments)

                results = search_documents(
                    arguments["query"]
                )

                tool_log.append({
                    "tool": item.name,
                    "arguments": arguments,
                    "results": results,
                })

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(results),
                })

        response = client.responses.create(
            model=settings.openai_model,
            instructions=INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS,
        )

    return {
        "answer": "Investigation reached the maximum number of tool steps.",
        "tool_calls": tool_log,
    }
