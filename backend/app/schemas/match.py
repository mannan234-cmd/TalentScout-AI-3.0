from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
import uuid

MatchStatus = Literal["suggested", "shortlisted", "application_ready", "applied", "dismissed"]


class Match(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    opportunity_id: str
    score: float  # 0..100
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    rationale: str = ""
    status: MatchStatus = "suggested"
    created_at: datetime = Field(default_factory=datetime.utcnow)
