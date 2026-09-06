"""
Common base for all pipeline agents. Each agent is a small, single-purpose
unit that takes typed input and returns typed output — the orchestrator
wires them together and enforces the human-in-the-loop gate between
Evidence/Signals and Matching.
"""
from abc import ABC, abstractmethod
from datetime import datetime


class BaseAgent(ABC):
    name: str = "base_agent"

    def log(self, message: str) -> None:
        # Simple stdout logging; swap for structured logging in production.
        print(f"[{datetime.utcnow().isoformat()}Z] [{self.name}] {message}")

    @abstractmethod
    def run(self, *args, **kwargs):
        ...
