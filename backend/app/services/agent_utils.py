import json


def clean_json_response(content):

    cleaned = content.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "")

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()


def parse_json(content):

    cleaned = clean_json_response(content)

    return json.loads(cleaned)