import json
import time

from openai import OpenAI

from app.agents.tools import search_documents
from app.agents.sql_tool import query_operations
from app.agents.memory import save_message, get_history
from app.core.config import settings


client = OpenAI(api_key=settings.openai_api_key)


TOOLS = [
    {
        "type": "function",
        "name": "search_documents",
        "description": "Search internal operations documents for incidents, staffing reports, and other written evidence.",
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
    },
    {
        "type": "function",
        "name": "query_operations",
        "description": "Query structured operational metrics such as throughput, staffing, and downtime for a site.",
        "parameters": {
            "type": "object",
            "properties": {
                "site": {
                    "type": "string"
                }
            },
            "required": ["site"],
            "additionalProperties": False,
        },
    },
]


INSTRUCTIONS = """
You are OpsIntel, an enterprise operations investigation agent.

Use the available tools to gather evidence before answering.

Use search_documents for written reports and incident evidence.
Use query_operations for structured metrics such as throughput,
staffing, and downtime.

When useful, use both tools.

Give a concise response with:
- Finding
- Evidence
- Likely cause
- Recommended action

Once you have enough evidence, stop using tools and provide the final answer.
"""


def investigate(question: str, session_id: str = "default"):
    start_time = time.perf_counter()
    history = get_history(session_id)

    save_message(
        session_id,
        "user",
        question,
    )

    conversation = history + [
        {
            "role": "user",
            "content": question,
        }
    ]
    response = client.responses.create(
        model=settings.openai_model,
        instructions=INSTRUCTIONS,
        input=conversation,
        tools=TOOLS,
    )

    tool_log = []

    for _ in range(6):
        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            answer = response.output_text

            save_message(
                session_id,
                "assistant",
                answer,
            )

            elapsed_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            return {
                "answer": answer,
                "tool_calls": tool_log,
                "session_id": session_id,
                "latency_ms": elapsed_ms,
                "tool_call_count": len(tool_log),
            }

        tool_outputs = []

        for item in function_calls:
            arguments = json.loads(item.arguments)

            if item.name == "search_documents":
                result = search_documents(
                    arguments["query"]
                )

            elif item.name == "query_operations":
                result = query_operations(
                    arguments["site"]
                )

                for row in result:
                    if "timestamp" in row:
                        row["timestamp"] = row["timestamp"].isoformat()

            else:
                continue

            tool_log.append({
                "tool": item.name,
                "arguments": arguments,
                "results": result,
            })

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result),
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
