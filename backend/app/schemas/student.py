from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field
import uuid


ReviewStatus = Literal[
    "new", "processing", "pending_review", "approved", "rejected"
]


class StudentSubmit(BaseModel):
    """Payload a candidate submits from the frontend portal."""
    full_name: str
    email: EmailStr
    university: str
    degree_program: str
    graduation_year: int
    skills: list[str] = Field(default_factory=list)
    bio: str = ""
    portfolio_url: Optional[str] = None
    evidence_text: str = ""  # raw evidence: project descriptions, achievements, etc.


class Student(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    full_name: str
    email: EmailStr
    university: str
    degree_program: str
    graduation_year: int
    skills: list[str] = Field(default_factory=list)
    bio: str = ""
    portfolio_url: Optional[str] = None
    evidence_text: str = ""

    status: ReviewStatus = "new"
    category: Optional[str] = None          # set by Discovery Agent
    potential_score: Optional[float] = None  # set by Evidence & Signals Agent
    is_high_potential: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None
