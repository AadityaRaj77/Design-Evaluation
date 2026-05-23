from openai import AsyncOpenAI

from app.core.config import GROQ_API_KEY

from app.schemas.agent_schema import AgentResponse

from app.services.agent_utils import parse_json


client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


async def analyze_colors(
    vision_metrics
):

    prompt = f"""
You are a senior UI color and visual aesthetics expert.

Analyze ONLY:
- color harmony
- contrast quality
- saturation consistency
- accessibility
- vibrancy
- visual coherence
- emotional tone

Metrics:

{vision_metrics}

Return STRICT JSON:

{
    "score": number,

    "issues": [
        {
            "severity": "critical | medium | low",
            "title": "string",
            "reason": "string"
        }
    ],

    "suggestions": [
        {
            "priority": 1,
            "action": "string"
        }
    ]
}

Severity Guidelines:
- critical = major UX or hierarchy failure
- medium = noticeable quality degradation
- low = polish-level issue
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