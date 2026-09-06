"""
Abstract interfaces the rest of the app codes against. Agents and services
never import a concrete provider directly — they get one from
`get_data_provider()` / `get_ai_provider()` in this package's __init__, so
switching DATA_PROVIDER or AI_PROVIDER in .env changes behaviour with zero
code changes elsewhere.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseDataProvider(ABC):
    """CRUD contract for whatever storage backend is in use."""

    # --- users ---
    @abstractmethod
    def create_user(self, user: dict) -> dict: ...
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[dict]: ...
    @abstractmethod
    def get_user(self, user_id: str) -> Optional[dict]: ...
    @abstractmethod
    def update_user(self, user_id: str, patch: dict) -> Optional[dict]: ...

    # --- students ---
    @abstractmethod
    def create_student(self, student: dict) -> dict: ...
    @abstractmethod
    def get_student(self, student_id: str) -> Optional[dict]: ...
    @abstractmethod
    def update_student(self, student_id: str, patch: dict) -> Optional[dict]: ...
    @abstractmethod
    def list_students(self, status: Optional[str] = None) -> list[dict]: ...

    # --- evidence ---
    @abstractmethod
    def add_evidence(self, evidence: dict) -> dict: ...
    @abstractmethod
    def list_evidence(self, student_id: str) -> list[dict]: ...

    # --- signals ---
    @abstractmethod
    def upsert_signal_report(self, report: dict) -> dict: ...
    @abstractmethod
    def get_signal_report(self, student_id: str) -> Optional[dict]: ...

    # --- opportunities ---
    @abstractmethod
    def create_opportunity(self, opp: dict) -> dict: ...
    @abstractmethod
    def list_opportunities(self, active_only: bool = False) -> list[dict]: ...
    @abstractmethod
    def get_opportunity(self, opp_id: str) -> Optional[dict]: ...

    # --- matches ---
    @abstractmethod
    def create_match(self, match: dict) -> dict: ...
    @abstractmethod
    def list_matches(self, student_id: Optional[str] = None) -> list[dict]: ...
    @abstractmethod
    def get_match(self, match_id: str) -> Optional[dict]: ...
    @abstractmethod
    def update_match(self, match_id: str, patch: dict) -> Optional[dict]: ...

    # --- applications ---
    @abstractmethod
    def create_application(self, application: dict) -> dict: ...
    @abstractmethod
    def list_applications(self, student_id: Optional[str] = None) -> list[dict]: ...
    @abstractmethod
    def get_application(self, application_id: str) -> Optional[dict]: ...
    @abstractmethod
    def update_application(self, application_id: str, patch: dict) -> Optional[dict]: ...


class BaseAIProvider(ABC):
    """Contract for whatever generates signals/analysis and application text."""

    @abstractmethod
    def extract_signals(self, student: dict, evidence_texts: list[str]) -> dict:
        """Return a dict shaped like SignalReport (minus id/student_id)."""
        ...

    @abstractmethod
    def generate_cover_letter(self, student: dict, opportunity: dict, match: dict) -> dict:
        """Return {'cover_letter': str, 'highlights': list[str]}."""
        ...
