"""
Matching Service — invokes the Matching Agent for an approved student and
persists resulting Match records. Only ever called after human approval
(review_service enforces the gate).
"""
from app.agents.matching_agent import MatchingAgent
from app.providers import get_data_provider

matching_agent = MatchingAgent()


def run_matching_for_student(student_id: str) -> list[dict]:
    data = get_data_provider()
    student = data.get_student(student_id)
    if not student:
        raise ValueError("Student not found")
    if student.get("status") != "approved":
        raise PermissionError(
            "Matching can only run for approved students. "
            "A human reviewer must Approve this candidate first."
        )

    signal_report = data.get_signal_report(student_id)
    opportunities = data.list_opportunities(active_only=True)

    raw_matches = matching_agent.run(student, signal_report, opportunities)
    persisted = [data.create_match(m) for m in _stamp(raw_matches)]
    return persisted


def _stamp(matches: list[dict]) -> list[dict]:
    import uuid
    from datetime import datetime
    for m in matches:
        m["id"] = str(uuid.uuid4())
        m["created_at"] = datetime.utcnow()
    return matches
