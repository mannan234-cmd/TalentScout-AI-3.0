"""
Tests the Gmail-connect + Send Application flow end-to-end using the real
FastAPI app, with smtplib.SMTP mocked out so no real network call is made.
"""
import uuid
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.__enter__()


def _signup_and_submit_approved_application():
    """Helper: get a student all the way to having a generated application."""
    unique_email = f"bilal.test.{uuid.uuid4().hex[:8]}@example.com"
    signup_res = client.post("/api/auth/signup", json={
        "full_name": "Bilal Test",
        "email": unique_email,
        "password": "testpass123",
        "role": "student",
    })
    token = signup_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    submit_res = client.post("/api/students/submit", json={
        "full_name": "Bilal Test",
        "email": unique_email,
        "university": "FAST NUCES",
        "degree_program": "BS Data Science",
        "graduation_year": 2027,
        "skills": ["python", "sql", "excel", "data analysis"],
        "bio": "Aspiring data analyst.",
        "portfolio_url": "https://github.com/bilal-test",
        "evidence_text": "Built a Power BI dashboard using SQL and Excel for a retail dataset.",
    }, headers=headers)
    student = submit_res.json()

    admin_login = client.post("/api/auth/login", json={"email": "admin@talentscout.ai", "password": "admin123"})
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
    client.post(f"/api/review/{student['id']}/decision", json={"decision": "approve"}, headers=admin_headers)

    matches = client.get(f"/api/matches?student_id={student['id']}", headers=admin_headers).json()
    assert len(matches) > 0
    match_id = matches[0]["id"]

    app_res = client.post(f"/api/applications/generate/{match_id}", headers=headers)
    return headers, app_res.json()


def test_send_application_requires_gmail_connection_first():
    headers, application = _signup_and_submit_approved_application()
    res = client.post(f"/api/applications/{application['id']}/send", headers=headers)
    assert res.status_code == 400
    assert "Connect your Gmail" in res.json()["detail"]


def test_connect_gmail_and_send_application_success():
    headers, application = _signup_and_submit_approved_application()

    connect_res = client.post("/api/email/connect", json={
        "gmail_address": "bilal.test@gmail.com",
        "app_password": "fake-app-password-1234",
    }, headers=headers)
    assert connect_res.status_code == 200
    assert connect_res.json()["connected"] is True

    status_res = client.get("/api/email/status", headers=headers)
    assert status_res.json()["connected"] is True

    with patch("app.api.endpoints.send_application_email") as mock_send:
        mock_send.return_value = None
        send_res = client.post(f"/api/applications/{application['id']}/send", headers=headers)

    assert send_res.status_code == 200
    body = send_res.json()
    assert body["sent"] is True
    assert body["sent_to"]
    mock_send.assert_called_once()
    _, kwargs = mock_send.call_args
    assert kwargs["gmail_address"] == "bilal.test@gmail.com"


def test_smtp_auth_failure_surfaces_as_502():
    headers, application = _signup_and_submit_approved_application()
    client.post("/api/email/connect", json={
        "gmail_address": "bilal.test@gmail.com",
        "app_password": "wrong-password",
    }, headers=headers)

    from app.services.email_service import EmailSendError
    with patch("app.api.endpoints.send_application_email", side_effect=EmailSendError("bad creds")):
        res = client.post(f"/api/applications/{application['id']}/send", headers=headers)

    assert res.status_code == 502
