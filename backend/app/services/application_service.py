"""
Application Service — invokes the Application Agent for a shortlisted match
and persists the resulting ApplicationPackage.
"""
import uuid
from datetime import datetime

from app.agents.application_agent import ApplicationAgent
from app.providers import get_data_provider

application_agent = ApplicationAgent()


def generate_application(match_id: str) -> dict:
    data = get_data_provider()
    match = data.get_match(match_id)
    if not match:
        raise ValueError("Match not found")

    student = data.get_student(match["student_id"])
    if not student or student.get("status") != "approved":
        raise PermissionError("Student must be approved before generating an application.")

    opportunity = data.get_opportunity(match["opportunity_id"])
    if not opportunity:
        raise ValueError("Opportunity not found")

    result = application_agent.run(student, opportunity, match)

    package = {
        "id": str(uuid.uuid4()),
        "match_id": match_id,
        "student_id": student["id"],
        "opportunity_id": opportunity["id"],
        "cover_letter": result["cover_letter"],
        "highlights": result.get("highlights", []),
        "generated_by": result.get("generated_by", "demo"),
        "created_at": datetime.utcnow(),
    }
    saved = data.create_application(package)
    data.update_match(match_id, {"status": "application_ready"})
    return saved
