from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class ApplicationPackage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    match_id: str
    student_id: str
    opportunity_id: str
    cover_letter: str
    highlights: list[str] = Field(default_factory=list)
    generated_by: str = "demo"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # email delivery status — set once the student sends it via their
    # connected Gmail account (see services/email_service.py)
    sent: bool = False
    sent_at: datetime | None = None
    sent_to: str | None = None
