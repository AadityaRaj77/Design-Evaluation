from pydantic import BaseModel
from typing import List


class AgentIssue(BaseModel):
    severity: str
    title: str
    reason: str


class AgentSuggestion(BaseModel):
    priority: int
    action: str


class AgentResponse(BaseModel):
    score: float
    issues: List[AgentIssue]
    suggestions: List[AgentSuggestion]