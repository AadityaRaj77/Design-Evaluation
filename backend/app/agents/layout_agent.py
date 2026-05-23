from openai import AsyncOpenAI

from app.core.config import GROQ_API_KEY

from app.schemas.agent_schema import AgentResponse

from app.services.agent_utils import parse_json


client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


async def analyze_layout(
    vision_metrics,
    memory_context=None
):

    prompt = f"""
You are a senior UI layout expert.

Analyze ONLY:
- spacing
- alignment
- whitespace
- visual balance
- clutter
- section organization

Metrics:

{vision_metrics}

Historical Similar Analyses:

{memory_context}

Return STRICT JSON:

{{
    "score": number,
    "issues": [],
    "suggestions": []
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

    validated = AgentResponse(**parsed)

    return validated.model_dump()