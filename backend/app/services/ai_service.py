import base64
import json

from openai import AsyncOpenAI

from app.core.config import GROQ_API_KEY
from app.prompts.critique_prompt import DESIGN_CRITIQUE_PROMPT
from app.schemas.response_schema import DesignReviewResponse
from app.core.logger import logger


client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


async def analyze_ui_image(image_bytes):

    logger.info("Starting UI analysis")

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    logger.info("Sending request to Groq vision model")

    response = await client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": DESIGN_CRITIQUE_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this UI screenshot critically."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.4
    )

    logger.info("Received response from model")

    content = response.choices[0].message.content

    try:

        cleaned = content.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "")

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        parsed = json.loads(cleaned)

        logger.info("JSON parsed successfully")

        validated = DesignReviewResponse(**parsed)

        logger.info("Response schema validated successfully")

        return validated.model_dump()

    except Exception as e:

        logger.error(f"Parsing failed: {str(e)}")

        return {
            "error": "Invalid JSON response",
            "raw_response": content,
            "exception": str(e)
        }