"""Tool implementations and OpenAI tool schemas for the profile chatbot."""

from __future__ import annotations

import json


def record_user_details(email, name="Name not provided", notes="not provided"):
    print(f"[tool] record_user_details: {name=} {email=} {notes=}")
    return "OK"


def record_recommended_company(company_name):
    print(f"[tool] record_recommended_company: {company_name=}")
    return "OK"


record_user_details_json = {
    "name": "record_user_details",
    "description": (
        "Use this tool to record that a user is interested in being in touch "
        "and provided an email address"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation worth recording",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_recommended_company_json = {
    "name": "record_recommended_company",
    "description": "Use this tool to record company name that user recommend",
    "parameters": {
        "type": "object",
        "properties": {
            "company_name": {
                "type": "string",
                "description": "The company name that user recommend",
            },
        },
        "required": ["company_name"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_recommended_company_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_recommended_company": record_recommended_company,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else f"Unknown tool: {tool_name}"
        results.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id,
            }
        )
    return results
