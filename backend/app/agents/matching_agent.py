"""
Matching Agent — auto-evaluates an APPROVED candidate's skills against every
active opportunity's required skills and produces scored Match records.
This agent only ever runs after human approval (enforced by the orchestrator
/ review_service, not by this agent itself, so the gate is explicit and
auditable at the service layer).
"""
from app.agents.base_agent import BaseAgent


class MatchingAgent(BaseAgent):
    name = "matching_agent"

    SHORTLIST_THRESHOLD = 55.0

    def run(self, student: dict, signal_report: dict | None, opportunities: list[dict]) -> list[dict]:
        detected = {
            d["skill"].lower(): d["confidence"]
            for d in (signal_report or {}).get("detected_skills", [])
        }
        # Fall back to claimed skills at moderate confidence if no signal report exists.
        if not detected:
            detected = {s.lower(): 0.5 for s in student.get("skills", [])}

        matches = []
        for opp in opportunities:
            required = [r.lower() for r in opp.get("required_skills", [])]
            if not required:
                continue
            matched = [r for r in required if r in detected]
            missing = [r for r in required if r not in detected]

            coverage = len(matched) / len(required)  # 0..1
            avg_conf = (sum(detected[m] for m in matched) / len(matched)) if matched else 0
            score = round(min(100.0, coverage * 70 + avg_conf * 30), 1)

            if score <= 0:
                continue

            rationale = (
                f"Matches {len(matched)}/{len(required)} required skill(s) "
                f"({round(coverage * 100)}% coverage) with average confidence "
                f"{round(avg_conf * 100)}%."
            )
            status = "shortlisted" if score >= self.SHORTLIST_THRESHOLD else "suggested"

            matches.append({
                "student_id": student["id"],
                "opportunity_id": opp["id"],
                "score": score,
                "matched_skills": matched,
                "missing_skills": missing,
                "rationale": rationale,
                "status": status,
            })

        matches.sort(key=lambda m: -m["score"])
        self.log(f"Generated {len(matches)} match(es) for student {student.get('id')}")
        return matches
