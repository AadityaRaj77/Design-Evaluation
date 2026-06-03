import json

from openai import AsyncOpenAI

from app.core.config import GROQ_API_KEY
from app.services.agent_utils import parse_json


client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


async def refine_critique(
    aggregated_result,
    evaluation
):
    prompt = f"""
You are an expert AI critique refinement system.

Your task:
Improve the following design critique.

Evaluator Feedback:
{json.dumps(evaluation, indent=2)}

Original Critique:
{json.dumps(aggregated_result, indent=2)}

Goals:
- remove generic advice
- increase specificity
- improve actionability
- remove redundancy
- improve clarity
- strengthen reasoning

Return STRICT JSON:

{{
    "refined_summary": {{
        "strength": "string",
        "weakness": "string"
    }},
    "refined_issues": [],
    "refined_suggestions": []
}}

Rewrite weak insights into highly specific professional UI critique.

Every suggestion must:
- reference a concrete issue
- explain impact on UX or aesthetics
- propose realistic improvement

Avoid:
- generic wording
- broad statements
- repetitive phrasing

Return ONLY valid JSON. No markdown. No explanation.
"""

    response = await client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON. No markdown. No prose."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content
    parsed = parse_json(content)
    return parsed