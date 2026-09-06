from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
import uuid

OpportunityType = Literal["internship", "scholarship", "job"]


class OpportunityCreate(BaseModel):
    title: str
    organization: str
    type: OpportunityType = "internship"
    description: str = ""
    required_skills: list[str] = Field(default_factory=list)
    location: str = "Remote"
    is_active: bool = True
    contact_email: str | None = None  # where applications get emailed to


class Opportunity(OpportunityCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
