from fastapi.testclient import TestClient
from app.main import app

# Using a context manager ensures FastAPI's startup event (which seeds demo
# data: admin account, sample opportunities, etc.) actually runs.
client = TestClient(app)
client.__enter__()


def test_root_health():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_signup_login_and_submit_flow():
    # signup a fresh student
    signup_res = client.post("/api/auth/signup", json={
        "full_name": "Ali Test",
        "email": "ali.test@example.com",
        "password": "testpass123",
        "role": "student",
    })
    assert signup_res.status_code == 200
    token = signup_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # submit a profile -> triggers autonomous pipeline, ends in pending_review
    submit_res = client.post("/api/students/submit", json={
        "full_name": "Ali Test",
        "email": "ali.test@example.com",
        "university": "FAST NUCES",
        "degree_program": "BS Software Engineering",
        "graduation_year": 2027,
        "skills": ["python", "react"],
        "bio": "Aspiring full-stack developer.",
        "portfolio_url": "https://github.com/ali-test",
        "evidence_text": "Built a React + FastAPI todo app with JWT auth and a Postgres backend.",
    }, headers=headers)
    assert submit_res.status_code == 200
    student = submit_res.json()
    assert student["status"] == "pending_review"
    assert student["category"] is not None
    assert student["potential_score"] is not None

    # admin approves -> should unblock matching
    admin_login = client.post("/api/auth/login", json={"email": "admin@talentscout.ai", "password": "admin123"})
    assert admin_login.status_code == 200
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    decision_res = client.post(f"/api/review/{student['id']}/decision",
                                json={"decision": "approve", "notes": "Looks solid."},
                                headers=admin_headers)
    assert decision_res.status_code == 200
    assert decision_res.json()["status"] == "approved"

    matches_res = client.get(f"/api/matches?student_id={student['id']}", headers=admin_headers)
    assert matches_res.status_code == 200
