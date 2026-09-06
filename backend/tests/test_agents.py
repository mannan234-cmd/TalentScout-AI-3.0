from app.agents.discovery_agent import DiscoveryAgent
from app.agents.matching_agent import MatchingAgent
from app.providers.demo_provider_ai import DemoAIProvider


def test_discovery_agent_categorizes_software_student():
    agent = DiscoveryAgent()
    student = {"id": "s1", "degree_program": "BS Computer Science",
               "bio": "I love python and machine learning", "skills": ["python"]}
    result = agent.run(student)
    assert result["category"] == "Software & AI"
    assert result["status"] == "processing"


def test_demo_ai_provider_extracts_signals():
    ai = DemoAIProvider()
    student = {"full_name": "Test User", "skills": ["python", "sql"],
               "bio": "I build dashboards", "portfolio_url": "https://github.com/x"}
    report = ai.extract_signals(student, ["Built a Power BI dashboard using SQL and Python."])
    assert report["potential_score"] > 0
    skills = [d["skill"] for d in report["detected_skills"]]
    assert "python" in skills
    assert "sql" in skills


def test_matching_agent_scores_and_shortlists():
    agent = MatchingAgent()
    student = {"id": "s1"}
    signal_report = {"detected_skills": [
        {"skill": "python", "confidence": 0.9, "evidence_snippet": ""},
        {"skill": "sql", "confidence": 0.8, "evidence_snippet": ""},
    ]}
    opportunities = [{
        "id": "o1", "required_skills": ["python", "sql", "excel"],
    }]
    matches = agent.run(student, signal_report, opportunities)
    assert len(matches) == 1
    assert matches[0]["opportunity_id"] == "o1"
    assert 0 < matches[0]["score"] <= 100
