from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth import hash_password, verify_password, create_access_token
from app.api.dependencies import get_current_user, require_role
from app.providers import get_data_provider
from app.services.orchestrator import run_intake_pipeline
from app.services import review_service, matching_service, application_service

from app.schemas.user import UserSignup, UserLogin, UserOut, Token, GmailConnect
from app.schemas.student import StudentSubmit, Student
from app.schemas.review import ReviewDecision
from app.schemas.opportunity import OpportunityCreate
from app.services.email_service import send_application_email, EmailSendError

import uuid
from datetime import datetime

router = APIRouter()


def _user_out(u: dict) -> dict:
    return {"id": u["id"], "full_name": u["full_name"], "email": u["email"],
            "role": u["role"], "student_id": u.get("student_id"),
            "gmail_connected": bool(u.get("gmail_address"))}


# ---------------------------------------------------------------- AUTH -----
@router.post("/auth/signup", response_model=Token, tags=["auth"])
def signup(payload: UserSignup):
    data = get_data_provider()
    if data.get_user_by_email(payload.email):
        raise HTTPException(400, "Email already registered")

    user = {
        "id": str(uuid.uuid4()),
        "full_name": payload.full_name,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "role": payload.role,
        "student_id": None,
        "created_at": datetime.utcnow(),
    }
    data.create_user(user)
    token = create_access_token(user["id"], user["role"])
    return {"access_token": token, "user": _user_out(user)}


@router.post("/auth/login", response_model=Token, tags=["auth"])
def login(payload: UserLogin):
    data = get_data_provider()
    user = data.get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(401, "Invalid email or password")
    token = create_access_token(user["id"], user["role"])
    return {"access_token": token, "user": _user_out(user)}


@router.get("/auth/me", response_model=UserOut, tags=["auth"])
def me(user: dict = Depends(get_current_user)):
    return _user_out(user)


# ------------------------------------------------------------- STUDENTS ----
@router.post("/students/submit", response_model=Student, tags=["students"])
def submit_student(payload: StudentSubmit, user: dict = Depends(get_current_user)):
    """
    Candidate submits their profile/evidence from the frontend portal.
    Automatically triggers Discovery -> Evidence -> Signals, then pauses
    for human review.
    """
    data = get_data_provider()
    student = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        **payload.model_dump(),
        "status": "new",
        "category": None,
        "potential_score": None,
        "is_high_potential": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": None,
    }
    data.create_student(student)
    student = run_intake_pipeline(student)

    if user.get("role") == "student" and not user.get("student_id"):
        user["student_id"] = student["id"]
    return student


@router.get("/students", response_model=list[Student], tags=["students"])
def list_students(status: str | None = None, user: dict = Depends(require_role("admin", "reviewer"))):
    data = get_data_provider()
    return data.list_students(status=status)


@router.get("/students/{student_id}", response_model=Student, tags=["students"])
def get_student(student_id: str, user: dict = Depends(get_current_user)):
    data = get_data_provider()
    student = data.get_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    if user.get("role") == "student" and student.get("user_id") != user["id"]:
        raise HTTPException(403, "Not your profile")
    return student


@router.get("/students/{student_id}/evidence", tags=["students"])
def get_evidence(student_id: str, user: dict = Depends(get_current_user)):
    data = get_data_provider()
    return data.list_evidence(student_id)


@router.get("/students/{student_id}/signals", tags=["students"])
def get_signals(student_id: str, user: dict = Depends(get_current_user)):
    data = get_data_provider()
    report = data.get_signal_report(student_id)
    if not report:
        raise HTTPException(404, "No signal report yet")
    return report


@router.get("/students/me/profile", response_model=Student, tags=["students"])
def my_profile(user: dict = Depends(require_role("student"))):
    data = get_data_provider()
    matches = [s for s in data.list_students() if s.get("user_id") == user["id"]]
    if not matches:
        raise HTTPException(404, "No profile submitted yet")
    return matches[0]


# --------------------------------------------------------------- REVIEW ----
@router.get("/review/queue", tags=["review"])
def review_queue(user: dict = Depends(require_role("admin", "reviewer"))):
    return review_service.list_queue()


@router.post("/review/{student_id}/decision", tags=["review"])
def review_decision(student_id: str, payload: ReviewDecision, user: dict = Depends(require_role("admin", "reviewer"))):
    try:
        if payload.decision == "approve":
            return review_service.approve(student_id, user["id"], payload.notes)
        return review_service.reject(student_id, user["id"], payload.notes)
    except (ValueError, PermissionError) as e:
        raise HTTPException(400, str(e))


# --------------------------------------------------------- OPPORTUNITIES ---
@router.post("/opportunities", tags=["opportunities"])
def create_opportunity(payload: OpportunityCreate, user: dict = Depends(require_role("admin", "reviewer"))):
    data = get_data_provider()
    opp = {"id": str(uuid.uuid4()), **payload.model_dump(), "created_at": datetime.utcnow()}
    return data.create_opportunity(opp)


@router.get("/opportunities", tags=["opportunities"])
def list_opportunities(active_only: bool = False, user: dict = Depends(get_current_user)):
    data = get_data_provider()
    return data.list_opportunities(active_only=active_only)


# --------------------------------------------------------------- MATCHES ---
@router.post("/matches/run/{student_id}", tags=["matches"])
def run_matches(student_id: str, user: dict = Depends(require_role("admin", "reviewer"))):
    try:
        return matching_service.run_matching_for_student(student_id)
    except (ValueError, PermissionError) as e:
        raise HTTPException(400, str(e))


@router.get("/matches", tags=["matches"])
def list_matches(student_id: str | None = None, user: dict = Depends(get_current_user)):
    data = get_data_provider()
    if user.get("role") == "student":
        my_students = [s["id"] for s in data.list_students() if s.get("user_id") == user["id"]]
        if student_id and student_id not in my_students:
            raise HTTPException(403, "Not your data")
        results = []
        for sid in ([student_id] if student_id else my_students):
            results.extend(data.list_matches(sid))
        return results
    return data.list_matches(student_id)


# ----------------------------------------------------------- APPLICATIONS -
@router.post("/applications/generate/{match_id}", tags=["applications"])
def generate_application(match_id: str, user: dict = Depends(get_current_user)):
    try:
        return application_service.generate_application(match_id)
    except (ValueError, PermissionError) as e:
        raise HTTPException(400, str(e))


@router.get("/applications", tags=["applications"])
def list_applications(student_id: str | None = None, user: dict = Depends(get_current_user)):
    data = get_data_provider()
    if user.get("role") == "student":
        my_students = [s["id"] for s in data.list_students() if s.get("user_id") == user["id"]]
        results = []
        for sid in ([student_id] if student_id else my_students):
            if student_id and sid not in my_students:
                continue
            results.extend(data.list_applications(sid))
        return results
    return data.list_applications(student_id)


# ------------------------------------------------------------------ EMAIL -
@router.post("/email/connect", tags=["email"])
def connect_gmail(payload: GmailConnect, user: dict = Depends(require_role("student"))):
    """
    Links the student's own Gmail account via a Gmail App Password so
    'Send Application' can email companies for real. See email_service.py
    for the security notes on how this is (and isn't) stored.
    """
    data = get_data_provider()
    data.update_user(user["id"], {
        "gmail_address": payload.gmail_address,
        "gmail_app_password": payload.app_password,
    })
    return {"connected": True, "gmail_address": payload.gmail_address}


@router.delete("/email/connect", tags=["email"])
def disconnect_gmail(user: dict = Depends(require_role("student"))):
    data = get_data_provider()
    data.update_user(user["id"], {"gmail_address": None, "gmail_app_password": None})
    return {"connected": False}


@router.get("/email/status", tags=["email"])
def email_status(user: dict = Depends(get_current_user)):
    return {"connected": bool(user.get("gmail_address")), "gmail_address": user.get("gmail_address")}


@router.post("/applications/{application_id}/send", tags=["email", "applications"])
def send_application(application_id: str, user: dict = Depends(require_role("student"))):
    """
    Actually emails the company contact for this application, from the
    student's own connected Gmail account, with the AI-generated cover
    letter as the message body. This is a real SMTP send — not a mock.
    """
    data = get_data_provider()

    application = data.get_application(application_id)
    if not application:
        raise HTTPException(404, "Application not found")

    student = data.get_student(application["student_id"])
    if not student or student.get("user_id") != user["id"]:
        raise HTTPException(403, "Not your application")

    if not user.get("gmail_address") or not user.get("gmail_app_password"):
        raise HTTPException(400, "Connect your Gmail account first (Settings -> Connect Gmail).")

    opportunity = data.get_opportunity(application["opportunity_id"])
    if not opportunity:
        raise HTTPException(404, "Opportunity not found")

    to_email = opportunity.get("contact_email")
    if not to_email:
        raise HTTPException(
            400,
            f"'{opportunity['title']}' has no contact email on file, so this "
            "application can't be auto-sent. You can still copy the cover "
            "letter and apply manually.",
        )

    subject = f"Application for {opportunity['title']} — {student['full_name']}"
    body = application["cover_letter"]
    if student.get("portfolio_url"):
        body += f"\n\nPortfolio: {student['portfolio_url']}"

    try:
        send_application_email(
            gmail_address=user["gmail_address"],
            app_password=user["gmail_app_password"],
            to_email=to_email,
            subject=subject,
            body=body,
            reply_to=student.get("email"),
        )
    except EmailSendError as e:
        raise HTTPException(502, str(e))

    updated = data.update_application(application_id, {
        "sent": True,
        "sent_at": datetime.utcnow(),
        "sent_to": to_email,
    })
    data.update_match(application["match_id"], {"status": "applied"})
    return updated


# ------------------------------------------------------------- ANALYTICS --
@router.get("/analytics", tags=["analytics"])
def analytics(user: dict = Depends(require_role("admin", "reviewer"))):
    data = get_data_provider()
    students = data.list_students()
    return {
        "total_students": len(students),
        "pending_human_reviews": len([s for s in students if s["status"] == "pending_review"]),
        "high_potential_candidates": len([s for s in students if s.get("is_high_potential")]),
        "active_opportunities": len(data.list_opportunities(active_only=True)),
        "approved_matches": len([m for m in data.list_matches() if m["status"] in ("shortlisted", "application_ready", "applied")]),
        "approved_students": len([s for s in students if s["status"] == "approved"]),
        "rejected_students": len([s for s in students if s["status"] == "rejected"]),
    }
