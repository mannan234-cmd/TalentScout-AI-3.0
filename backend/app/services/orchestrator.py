"""
Orchestrator — wires the autonomous agents together for the parts of the
pipeline that run WITHOUT human input (Discovery -> Evidence -> Signals),
then stops and marks the student `pending_review`. Nothing past that point
runs until review_service.approve() is called by an admin/reviewer.
"""
from app.agents.discovery_agent import DiscoveryAgent
from app.agents.evidence_agent import EvidenceAgent
from app.agents.signals_agent import SignalsAgent
from app.providers import get_data_provider

discovery_agent = DiscoveryAgent()
evidence_agent = EvidenceAgent()
signals_agent = SignalsAgent()


HIGH_POTENTIAL_THRESHOLD = 70.0


def run_intake_pipeline(student: dict) -> dict:
    """
    Runs the autonomous, pre-review portion of the pipeline for a freshly
    submitted student:
      1. Discovery Agent -> category
      2. Evidence Agent -> structured evidence items (persisted)
      3. Signals Agent -> SignalReport + potential_score (persisted)
      4. Student status set to `pending_review` (blocks Matching/Application
         until a human explicitly approves via review_service).
    Returns the fully updated student dict.
    """
    data = get_data_provider()

    # 1. Discovery
    patch = discovery_agent.run(student)
    student = data.update_student(student["id"], patch)

    # 2. Evidence parsing + persistence
    evidence_items = evidence_agent.run(student["id"], student.get("evidence_text", ""))
    persisted_evidence = []
    for item in evidence_items:
        import uuid
        from datetime import datetime
        item["id"] = str(uuid.uuid4())
        item["created_at"] = datetime.utcnow()
        persisted_evidence.append(data.add_evidence(item))

    # 3. Signals / scoring
    report = signals_agent.run(student, persisted_evidence)
    import uuid
    from datetime import datetime
    report["id"] = str(uuid.uuid4())
    report["student_id"] = student["id"]
    report.setdefault("created_at", datetime.utcnow())
    data.upsert_signal_report(report)

    is_high_potential = report.get("potential_score", 0) >= HIGH_POTENTIAL_THRESHOLD

    # 4. Gate for human review
    student = data.update_student(student["id"], {
        "status": "pending_review",
        "potential_score": report.get("potential_score", 0),
        "is_high_potential": is_high_potential,
    })
    return student
