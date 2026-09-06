"""
Supabase-backed data provider (optional — used when DATA_PROVIDER=supabase).

This is a thin adapter over the `supabase-py` client. It expects tables named
users, students, evidence, signal_reports, opportunities, matches,
applications with columns matching the pydantic schema field names.

Not required for the demo to run — the app falls back to DemoDataProvider
whenever DATA_PROVIDER != "supabase" or the supabase package / credentials
are missing, so importing this module is safe even without the dependency
installed as long as it is not instantiated.
"""
from typing import Optional
from app.providers.base_provider import BaseDataProvider
from app.config import get_settings


class SupabaseDataProvider(BaseDataProvider):
    def __init__(self):
        try:
            from supabase import create_client
        except ImportError as e:
            raise RuntimeError(
                "supabase-py is not installed. Run `pip install supabase` "
                "or set DATA_PROVIDER=demo in .env."
            ) from e

        settings = get_settings()
        if not settings.supabase_url or not settings.supabase_key:
            raise RuntimeError(
                "SUPABASE_URL / SUPABASE_KEY are not set in .env. "
                "Set DATA_PROVIDER=demo to use the built-in in-memory store instead."
            )
        self.client = create_client(settings.supabase_url, settings.supabase_key)

    # --- users ---
    def create_user(self, user: dict) -> dict:
        self.client.table("users").insert(user).execute()
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        res = self.client.table("users").select("*").eq("email", email).limit(1).execute()
        return res.data[0] if res.data else None

    def get_user(self, user_id: str) -> Optional[dict]:
        res = self.client.table("users").select("*").eq("id", user_id).limit(1).execute()
        return res.data[0] if res.data else None

    def update_user(self, user_id: str, patch: dict) -> Optional[dict]:
        self.client.table("users").update(patch).eq("id", user_id).execute()
        return self.get_user(user_id)

    # --- students ---
    def create_student(self, student: dict) -> dict:
        self.client.table("students").insert(student).execute()
        return student

    def get_student(self, student_id: str) -> Optional[dict]:
        res = self.client.table("students").select("*").eq("id", student_id).limit(1).execute()
        return res.data[0] if res.data else None

    def update_student(self, student_id: str, patch: dict) -> Optional[dict]:
        self.client.table("students").update(patch).eq("id", student_id).execute()
        return self.get_student(student_id)

    def list_students(self, status: Optional[str] = None) -> list[dict]:
        q = self.client.table("students").select("*")
        if status:
            q = q.eq("status", status)
        res = q.order("created_at", desc=True).execute()
        return res.data or []

    # --- evidence ---
    def add_evidence(self, evidence: dict) -> dict:
        self.client.table("evidence").insert(evidence).execute()
        return evidence

    def list_evidence(self, student_id: str) -> list[dict]:
        res = self.client.table("evidence").select("*").eq("student_id", student_id).execute()
        return res.data or []

    # --- signals ---
    def upsert_signal_report(self, report: dict) -> dict:
        self.client.table("signal_reports").upsert(report, on_conflict="student_id").execute()
        return report

    def get_signal_report(self, student_id: str) -> Optional[dict]:
        res = self.client.table("signal_reports").select("*").eq("student_id", student_id).limit(1).execute()
        return res.data[0] if res.data else None

    # --- opportunities ---
    def create_opportunity(self, opp: dict) -> dict:
        self.client.table("opportunities").insert(opp).execute()
        return opp

    def list_opportunities(self, active_only: bool = False) -> list[dict]:
        q = self.client.table("opportunities").select("*")
        if active_only:
            q = q.eq("is_active", True)
        res = q.order("created_at", desc=True).execute()
        return res.data or []

    def get_opportunity(self, opp_id: str) -> Optional[dict]:
        res = self.client.table("opportunities").select("*").eq("id", opp_id).limit(1).execute()
        return res.data[0] if res.data else None

    # --- matches ---
    def create_match(self, match: dict) -> dict:
        self.client.table("matches").insert(match).execute()
        return match

    def list_matches(self, student_id: Optional[str] = None) -> list[dict]:
        q = self.client.table("matches").select("*")
        if student_id:
            q = q.eq("student_id", student_id)
        res = q.order("score", desc=True).execute()
        return res.data or []

    def get_match(self, match_id: str) -> Optional[dict]:
        res = self.client.table("matches").select("*").eq("id", match_id).limit(1).execute()
        return res.data[0] if res.data else None

    def update_match(self, match_id: str, patch: dict) -> Optional[dict]:
        self.client.table("matches").update(patch).eq("id", match_id).execute()
        return self.get_match(match_id)

    # --- applications ---
    def create_application(self, application: dict) -> dict:
        self.client.table("applications").insert(application).execute()
        return application

    def list_applications(self, student_id: Optional[str] = None) -> list[dict]:
        q = self.client.table("applications").select("*")
        if student_id:
            q = q.eq("student_id", student_id)
        res = q.order("created_at", desc=True).execute()
        return res.data or []

    def get_application(self, application_id: str) -> Optional[dict]:
        res = self.client.table("applications").select("*").eq("id", application_id).limit(1).execute()
        return res.data[0] if res.data else None

    def update_application(self, application_id: str, patch: dict) -> Optional[dict]:
        self.client.table("applications").update(patch).eq("id", application_id).execute()
        return self.get_application(application_id)
