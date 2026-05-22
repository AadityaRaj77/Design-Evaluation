from typing import Optional

from sqlmodel import SQLModel, Field


class ReviewMemory(
    SQLModel,
    table=True
):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    overall_score: float

    text_density: int

    whitespace_ratio: float

    edge_density: float

    spacing_consistency: float

    critique_summary: str

    created_at: str