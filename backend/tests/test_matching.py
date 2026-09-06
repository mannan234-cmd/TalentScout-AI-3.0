from app.agents.matching_agent import MatchingAgent


def test_no_match_when_no_required_skills():
    agent = MatchingAgent()
    student = {"id": "s1"}
    opportunities = [{"id": "o1", "required_skills": []}]
    matches = agent.run(student, {"detected_skills": []}, opportunities)
    assert matches == []


def test_missing_skills_reported():
    agent = MatchingAgent()
    student = {"id": "s1"}
    signal_report = {"detected_skills": [{"skill": "python", "confidence": 0.9, "evidence_snippet": ""}]}
    opportunities = [{"id": "o1", "required_skills": ["python", "react"]}]
    matches = agent.run(student, signal_report, opportunities)
    assert matches[0]["missing_skills"] == ["react"]
    assert matches[0]["matched_skills"] == ["python"]
