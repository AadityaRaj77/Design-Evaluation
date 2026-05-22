from pydantic import BaseModel
from typing import List, Dict


class Issue(BaseModel):
    severity: str
    title: str
    reason: str


class Suggestion(BaseModel):
    priority: int
    action: str


class DesignReviewResponse(BaseModel):
    overall_score: float
    confidence: float

    summary: Dict[str, str]

    metrics: Dict[str, float]

    issues: List[Issue]

    suggestions: List[Suggestion]