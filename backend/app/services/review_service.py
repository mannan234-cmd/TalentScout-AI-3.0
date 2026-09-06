"""
Review Service — the human-in-the-loop gate. AI agents only ever produce
*advisory* output (category, signals, potential_score); a human admin or
reviewer must call approve() here before Matching/Application ever run for
a given student.
"""
from datetime import datetime
from app.providers import get_data_provider
from app.services.matching_service import run_matching_for_student


def list_queue() -> list[dict]:
    data = get_data_provider()
    return data.list_students(status="pending_review")


def approve(student_id: str, reviewer_id: str, notes: str = "") -> dict:
    data = get_data_provider()
    student = data.get_student(student_id)
    if not student:
        raise ValueError("Student not found")
    if student.get("status") != "pending_review":
        raise PermissionError("Only students in 'pending_review' can be approved.")

    student = data.update_student(student_id, {
        "status": "approved",
        "reviewed_by": reviewer_id,
        "reviewed_at": datetime.utcnow(),
        "review_notes": notes,
    })

    # Approval automatically unblocks the Matching stage.
    try:
        run_matching_for_student(student_id)
    except Exception as e:
        # Approval itself must still succeed even if matching has no active
        # opportunities yet — surface a soft warning instead of failing.
        student["_matching_warning"] = str(e)

    return student


def reject(student_id: str, reviewer_id: str, notes: str = "") -> dict:
    data = get_data_provider()
    student = data.get_student(student_id)
    if not student:
        raise ValueError("Student not found")
    if student.get("status") != "pending_review":
        raise PermissionError("Only students in 'pending_review' can be rejected.")

    return data.update_student(student_id, {
        "status": "rejected",
        "reviewed_by": reviewer_id,
        "reviewed_at": datetime.utcnow(),
        "review_notes": notes,
    })
