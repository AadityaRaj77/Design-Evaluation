import json
import re


def clean_json_response(content):
    if not content:
        raise ValueError("Empty LLM response")

    cleaned = content.strip()

    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    return cleaned


def parse_json(content):

    if not content:
        raise ValueError(
            "Empty LLM response"
        )

    cleaned = content.strip()

    cleaned = cleaned.replace(
        "```json",
        ""
    )

    cleaned = cleaned.replace(
        "```",
        ""
    )

    cleaned = cleaned.strip()

    # FIRST try full content

    try:
        return json.loads(cleaned)

    except Exception:
        pass

    # FIND JSON START

    start = cleaned.find("{")

    if start == -1:
        raise ValueError(
            "No JSON object found"
        )

    decoder = json.JSONDecoder()

    try:

        parsed, _ = decoder.raw_decode(
            cleaned[start:]
        )

        return parsed

    except Exception:

        print("\nFAILED JSON:")
        print(cleaned)
        print("\nEND FAILED JSON\n")

        raise ValueError(
            "LLM did not return valid JSON"
        )