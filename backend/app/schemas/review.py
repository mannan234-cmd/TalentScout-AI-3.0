from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class ReviewDecision(BaseModel):
    decision: Literal["approve", "reject"]
    notes: str = ""


class ReviewQueueItem(BaseModel):
    student_id: str
    full_name: str
    email: str
    category: str | None = None
    potential_score: float | None = None
    is_high_potential: bool = False
    submitted_at: datetime
