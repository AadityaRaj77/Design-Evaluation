from sqlmodel import Session, select

from app.core.database import engine

from app.models.review_memory import (
    ReviewMemory
)


def retrieve_similar_reviews(
    vision_metrics,
    limit=3
):

    text_density = vision_metrics.get(
        "text_density",
        0
    )

    whitespace_ratio = vision_metrics.get(
        "whitespace_ratio",
        0
    )

    with Session(engine) as session:

        statement = (
            select(ReviewMemory)
        )

        results = session.exec(
            statement
        ).all()

    ranked = []

    for review in results:

        distance = (
            abs(
                review.text_density
                - text_density
            )
            +
            abs(
                review.whitespace_ratio
                - whitespace_ratio
            )
        )

        ranked.append(
            (distance, review)
        )

    ranked.sort(
        key=lambda x: x[0]
    )

    similar = [
        item[1]
        for item in ranked[:limit]
    ]

    return similar