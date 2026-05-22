from datetime import datetime

from sqlmodel import Session

from app.core.database import engine

from app.models.review_memory import (
    ReviewMemory
)


def store_review_memory(
    result,
    vision_metrics
):

    memory = ReviewMemory(

        overall_score=result.get(
            "overall_score",
            0
        ),

        text_density=vision_metrics.get(
            "text_density",
            0
        ),

        whitespace_ratio=vision_metrics.get(
            "whitespace_ratio",
            0
        ),

        edge_density=vision_metrics.get(
            "edge_density",
            0
        ),

        spacing_consistency=vision_metrics.get(
            "spacing_consistency",
            0
        ),

        critique_summary=result.get(
            "summary",
            {}
        ).get(
            "weakness",
            ""
        ),

        created_at=str(
            datetime.utcnow()
        )
    )

    with Session(engine) as session:

        session.add(memory)

        session.commit()