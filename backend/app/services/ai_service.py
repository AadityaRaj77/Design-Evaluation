import base64
import json

from openai import AsyncOpenAI

from app.core.config import GROQ_API_KEY
from app.prompts.critique_prompt import DESIGN_CRITIQUE_PROMPT
from app.schemas.response_schema import DesignReviewResponse
from app.core.logger import logger
from app.services.agent_utils import parse_json


client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


async def analyze_ui_image(image_bytes, vision_metrics):

    logger.info("Starting UI analysis")

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    logger.info("Sending request to Groq vision model")

    response = await client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
             "role": "system",
             "content": DESIGN_CRITIQUE_PROMPT + """

             IMPORTANT:
              Return ONLY valid JSON.
              Do not use markdown.
              Do not explain your reasoning.
              Do not add text before JSON.
              Do not add text after JSON.
            """
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                         Analyze this UI screenshot critically.

                         Additional extracted metrics:

                         {json.dumps(vision_metrics, indent=2)}

                         Use these measurable signals while evaluating:
                        - typography
                        - spacing
                        - hierarchy
                        - visual clarity
                        - density
                        - CTA prominence
                        """
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

        parsed = parse_json(content)

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