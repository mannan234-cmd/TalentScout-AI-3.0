"""
Evidence & Signals Agent — the analytical core: takes a student's profile +
parsed evidence and produces a SignalReport (detected skills, strengths,
gaps, and an overall potential score). Delegates the actual analysis to the
configured AI provider (demo rule-based engine, or Groq) so this agent stays
provider-agnostic.
"""
from app.agents.base_agent import BaseAgent
from app.providers import get_ai_provider


class SignalsAgent(BaseAgent):
    name = "signals_agent"

    def run(self, student: dict, evidence_items: list[dict]) -> dict:
        ai = get_ai_provider()
        evidence_texts = [e.get("description", "") for e in evidence_items]
        report = ai.extract_signals(student, evidence_texts)
        self.log(
            f"Generated signal report for student {student.get('id')} "
            f"(potential_score={report.get('potential_score')})"
        )
        return report
