"""
Demo data provider: an in-memory store (app.models.database.db).
Zero external dependencies — this is what makes the whole platform runnable
out of the box.
"""
from typing import Optional
from datetime import datetime

from app.models.database import db
from app.providers.base_provider import BaseDataProvider


class DemoDataProvider(BaseDataProvider):
    # --- users ---
    def create_user(self, user: dict) -> dict:
        db.users[user["id"]] = user
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        for u in db.users.values():
            if u["email"].lower() == email.lower():
                return u
        return None

    def get_user(self, user_id: str) -> Optional[dict]:
        return db.users.get(user_id)

    def update_user(self, user_id: str, patch: dict) -> Optional[dict]:
        u = db.users.get(user_id)
        if not u:
            return None
        u.update(patch)
        db.users[user_id] = u
        return u

    # --- students ---
    def create_student(self, student: dict) -> dict:
        db.students[student["id"]] = student
        return student

    def get_student(self, student_id: str) -> Optional[dict]:
        return db.students.get(student_id)

    def update_student(self, student_id: str, patch: dict) -> Optional[dict]:
        s = db.students.get(student_id)
        if not s:
            return None
        s.update(patch)
        s["updated_at"] = datetime.utcnow()
        db.students[student_id] = s
        return s

    def list_students(self, status: Optional[str] = None) -> list[dict]:
        items = list(db.students.values())
        if status:
            items = [s for s in items if s.get("status") == status]
        return sorted(items, key=lambda s: s["created_at"], reverse=True)

    # --- evidence ---
    def add_evidence(self, evidence: dict) -> dict:
        db.evidence[evidence["id"]] = evidence
        return evidence

    def list_evidence(self, student_id: str) -> list[dict]:
        return [e for e in db.evidence.values() if e["student_id"] == student_id]

    # --- signals ---
    def upsert_signal_report(self, report: dict) -> dict:
        db.signals[report["student_id"]] = report
        return report

    def get_signal_report(self, student_id: str) -> Optional[dict]:
        return db.signals.get(student_id)

    # --- opportunities ---
    def create_opportunity(self, opp: dict) -> dict:
        db.opportunities[opp["id"]] = opp
        return opp

    def list_opportunities(self, active_only: bool = False) -> list[dict]:
        items = list(db.opportunities.values())
        if active_only:
            items = [o for o in items if o.get("is_active")]
        return sorted(items, key=lambda o: o["created_at"], reverse=True)

    def get_opportunity(self, opp_id: str) -> Optional[dict]:
        return db.opportunities.get(opp_id)

    # --- matches ---
    def create_match(self, match: dict) -> dict:
        db.matches[match["id"]] = match
        return match

    def list_matches(self, student_id: Optional[str] = None) -> list[dict]:
        items = list(db.matches.values())
        if student_id:
            items = [m for m in items if m["student_id"] == student_id]
        return sorted(items, key=lambda m: m["score"], reverse=True)

    def get_match(self, match_id: str) -> Optional[dict]:
        return db.matches.get(match_id)

    def update_match(self, match_id: str, patch: dict) -> Optional[dict]:
        m = db.matches.get(match_id)
        if not m:
            return None
        m.update(patch)
        db.matches[match_id] = m
        return m

    # --- applications ---
    def create_application(self, application: dict) -> dict:
        db.applications[application["id"]] = application
        return application

    def list_applications(self, student_id: Optional[str] = None) -> list[dict]:
        items = list(db.applications.values())
        if student_id:
            items = [a for a in items if a["student_id"] == student_id]
        return sorted(items, key=lambda a: a["created_at"], reverse=True)

    def get_application(self, application_id: str) -> Optional[dict]:
        return db.applications.get(application_id)

    def update_application(self, application_id: str, patch: dict) -> Optional[dict]:
        a = db.applications.get(application_id)
        if not a:
            return None
        a.update(patch)
        db.applications[application_id] = a
        return a
