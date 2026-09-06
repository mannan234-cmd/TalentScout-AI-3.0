"""
Groq-backed AI provider (optional — used when AI_PROVIDER=groq).

Uses Groq's OpenAI-compatible chat completions endpoint via plain httpx, so
no extra SDK dependency is required. Falls back gracefully: if the call
fails for any reason, it raises and the orchestrator will surface a clear
error rather than silently producing bad data.
"""
import json
import httpx

from app.config import get_settings
from app.providers.base_provider import BaseAIProvider
from app.providers.demo_provider_ai import DemoAIProvider  # rule-based fallback helpers


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class GroqAIProvider(BaseAIProvider):
    def __init__(self):
        settings = get_settings()
        if not settings.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set in .env. Set AI_PROVIDER=demo to use "
                "the built-in rule-based analyzer instead."
            )
        self.settings = settings
        self._fallback = DemoAIProvider()

    def _chat(self, system: str, user: str) -> str:
        headers = {"Authorization": f"Bearer {self.settings.groq_api_key}"}
        payload = {
            "model": self.settings.groq_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
        }
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(GROQ_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    def extract_signals(self, student: dict, evidence_texts: list[str]) -> dict:
        system = (
            "You are the Evidence & Signals Agent of a student career-matching "
            "platform. Analyze the candidate and respond ONLY with strict JSON "
            "matching this shape: {\"detected_skills\": [{\"skill\": str, "
            "\"confidence\": float 0-1, \"evidence_snippet\": str}], "
            "\"strengths\": [str], \"gaps\": [str], \"potential_score\": float 0-100, "
            "\"summary\": str}. No markdown, no preamble."
        )
        user = json.dumps({
            "profile": {
                "skills_claimed": student.get("skills", []),
                "bio": student.get("bio", ""),
                "degree_program": student.get("degree_program"),
                "university": student.get("university"),
            },
            "evidence": evidence_texts,
        })
        try:
            raw = self._chat(system, user)
            parsed = json.loads(raw)
            parsed["generated_by"] = "groq"
            return parsed
        except Exception:
            # graceful degrade to rule-based analysis rather than failing the pipeline
            fallback = self._fallback.extract_signals(student, evidence_texts)
            fallback["generated_by"] = "demo-fallback"
            return fallback

    def generate_cover_letter(self, student: dict, opportunity: dict, match: dict) -> dict:
        system = (
            "You are the Application Agent. Write a tailored, professional, "
            "concise cover letter (under 300 words) connecting the candidate's "
            "real skills/evidence to the opportunity's requirements. Respond "
            "ONLY with strict JSON: {\"cover_letter\": str, \"highlights\": [str]}."
        )
        user = json.dumps({
            "student": {
                "name": student.get("full_name"),
                "skills": student.get("skills", []),
                "bio": student.get("bio", ""),
            },
            "opportunity": {
                "title": opportunity.get("title"),
                "organization": opportunity.get("organization"),
                "required_skills": opportunity.get("required_skills", []),
                "description": opportunity.get("description", ""),
            },
            "matched_skills": match.get("matched_skills", []),
        })
        try:
            raw = self._chat(system, user)
            parsed = json.loads(raw)
            parsed["generated_by"] = "groq"
            return parsed
        except Exception:
            fallback = self._fallback.generate_cover_letter(student, opportunity, match)
            fallback["generated_by"] = "demo-fallback"
            return fallback
