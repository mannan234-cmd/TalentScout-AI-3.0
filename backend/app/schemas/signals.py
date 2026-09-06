from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class SkillSignal(BaseModel):
    skill: str
    confidence: float  # 0..1
    evidence_snippet: str = ""


class SignalReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    detected_skills: list[SkillSignal] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    potential_score: float = 0.0  # 0..100
    summary: str = ""
    generated_by: str = "demo"  # which AI provider produced this
    created_at: datetime = Field(default_factory=datetime.utcnow)
