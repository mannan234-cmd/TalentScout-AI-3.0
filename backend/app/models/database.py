"""
In-memory "database" used by the demo data provider.

This intentionally mimics a set of tables (dicts keyed by id) so that
swapping to a real database (Supabase provider) later is a drop-in
replacement of the provider layer, not a rewrite of business logic.

NOTE: state resets whenever the process restarts. This is fine for a demo /
local dev environment. For persistence, switch DATA_PROVIDER=supabase in .env.
"""
from threading import Lock


class InMemoryDB:
    def __init__(self):
        self.lock = Lock()
        self.users: dict[str, dict] = {}
        self.students: dict[str, dict] = {}
        self.evidence: dict[str, dict] = {}       # id -> EvidenceItem dict
        self.signals: dict[str, dict] = {}        # student_id -> SignalReport dict
        self.opportunities: dict[str, dict] = {}
        self.matches: dict[str, dict] = {}
        self.applications: dict[str, dict] = {}


db = InMemoryDB()
