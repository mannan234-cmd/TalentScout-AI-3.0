"""
Application Agent — generates a personalized cover letter / application
packet for a SHORTLISTED match. Delegates text generation to the configured
AI provider.
"""
from app.agents.base_agent import BaseAgent
from app.providers import get_ai_provider


class ApplicationAgent(BaseAgent):
    name = "application_agent"

    def run(self, student: dict, opportunity: dict, match: dict) -> dict:
        ai = get_ai_provider()
        result = ai.generate_cover_letter(student, opportunity, match)
        self.log(
            f"Generated application package for student {student.get('id')} "
            f"-> opportunity {opportunity.get('id')}"
        )
        return result
