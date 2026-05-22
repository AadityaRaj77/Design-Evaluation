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

Evaluate the following design analysis outputs.

Detect:
- vague reasoning
- repetitive suggestions
- contradictions
- generic feedback
- weak specificity

Analysis:

{agent_outputs}

Return STRICT JSON:

{{
    "quality_score": number,
    "issues": [],
    "improvement_suggestions": []
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