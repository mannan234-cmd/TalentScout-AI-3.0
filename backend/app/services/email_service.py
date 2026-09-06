"""
Email Service — sends the actual application email on the student's behalf,
from the student's own Gmail account, using a Gmail App Password (NOT
OAuth, NOT the student's real password). This is a real SMTP send, not a
simulation.

How a student connects (see /api/email/connect):
  1. Student enables 2-Step Verification on their Google account.
  2. Student generates an "App Password" at
     https://myaccount.google.com/apppasswords
  3. Student pastes their Gmail address + that 16-character app password
     into TalentScout AI once.
  4. From then on, "Send Application" actually emails the company contact
     directly from the student's inbox, with the AI-generated cover letter
     as the body — a copy will also show up in the student's own Sent folder.

SECURITY NOTE (college-project scope): the app password is kept only in the
in-memory demo store for the lifetime of the process — it is never written
to disk and never returned to the frontend. For a real production deployment
this should instead use Gmail OAuth2 (no password sharing at all) and an
encrypted secrets store / vault. This SMTP approach is intentionally simple
so the feature is fully real and demoable without needing a Google Cloud
OAuth app to be provisioned.
"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GMAIL_SMTP_HOST = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587


class EmailSendError(Exception):
    pass


def send_application_email(
    gmail_address: str,
    app_password: str,
    to_email: str,
    subject: str,
    body: str,
    reply_to: str | None = None,
) -> None:
    """
    Sends a real email via Gmail's SMTP relay, authenticated as the
    student's own Gmail account. Raises EmailSendError with a
    human-readable message on any failure (bad app password, network
    issue, etc.) so the API layer can surface it cleanly.
    """
    msg = MIMEMultipart()
    msg["From"] = gmail_address
    msg["To"] = to_email
    msg["Subject"] = subject
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT, timeout=20) as server:
            server.starttls(context=context)
            server.login(gmail_address, app_password)
            server.sendmail(gmail_address, [to_email], msg.as_string())
    except smtplib.SMTPAuthenticationError as e:
        raise EmailSendError(
            "Gmail rejected the credentials. Make sure you generated an "
            "App Password (not your normal Gmail password) at "
            "myaccount.google.com/apppasswords."
        ) from e
    except (smtplib.SMTPException, OSError) as e:
        raise EmailSendError(f"Could not send email: {e}") from e
