"""
Evidence Agent — normalizes raw evidence submissions (project descriptions,
certificates, achievements) into structured EvidenceItem-shaped records and
extracts naive keyword tags from each, ahead of the deeper Signals Agent
analysis.
"""
import re
from app.agents.base_agent import BaseAgent
from app.providers.demo_provider_ai import SKILL_VOCAB, _find_keywords


class EvidenceAgent(BaseAgent):
    name = "evidence_agent"

    def run(self, student_id: str, evidence_text: str) -> list[dict]:
        """
        Split a raw evidence blob (candidates often paste multiple projects/
        achievements separated by blank lines or numbering) into discrete
        evidence items with extracted keyword tags.
        """
        if not evidence_text.strip():
            return []

        chunks = [c.strip() for c in re.split(r"\n\s*\n|\n?\d+\.\s", evidence_text) if c.strip()]
        items = []
        for chunk in chunks:
            title = chunk.split(".")[0][:80] or "Untitled evidence"
            keywords = _find_keywords(chunk, SKILL_VOCAB)
            items.append({
                "student_id": student_id,
                "type": "project",
                "title": title,
                "description": chunk,
                "extracted_keywords": keywords,
            })
        self.log(f"Parsed {len(items)} evidence item(s) for student {student_id}")
        return items
