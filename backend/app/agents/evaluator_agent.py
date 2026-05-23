from openai import AsyncOpenAI

from app.core.config import GROQ_API_KEY

from app.services.agent_utils import parse_json


client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


async def evaluate_agent_outputs(
    agent_outputs
):

    prompt = f"""
You are an expert AI critique evaluator.

Your job is to aggressively evaluate the quality
of design critique outputs produced by AI agents.

Critique aggressively.

Penalize:
- generic advice
- weak specificity
- repeated observations
- obvious design commentary
- non-actionable suggestions
- shallow reasoning
- hallucinated claims
- overlap between agents

A strong critique should:
- identify precise visual problems
- explain WHY they matter
- provide concrete improvement direction
- sound like a senior product designer

Analyze the following outputs:

{agent_outputs}

Return STRICT JSON:

{{
    "quality_score": number,

    "issues": [
        {{
            "severity": "critical | medium | low",
            "title": "string",
            "reason": "string"
        }}
    ],

    "improvement_suggestions": [
        {{
            "priority": 1,
            "action": "string"
        }}
    ]
}}
"""

    response = await client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
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