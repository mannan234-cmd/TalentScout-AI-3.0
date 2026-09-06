from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
import uuid

EvidenceType = Literal["project", "certificate", "achievement", "publication", "other"]


class EvidenceItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    type: EvidenceType = "other"
    title: str
    description: str = ""
    source_url: str | None = None
    extracted_keywords: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
