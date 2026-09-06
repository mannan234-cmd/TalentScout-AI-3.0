from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr, Field
import uuid

Role = Literal["admin", "reviewer", "student"]


class UserSignup(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Role = "student"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    email: EmailStr
    hashed_password: str
    role: Role = "student"
    student_id: str | None = None  # linked Student record, if role == student
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: Role
    student_id: str | None = None
    gmail_connected: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class GmailConnect(BaseModel):
    """
    Student links their own Gmail account using a Gmail App Password
    (myaccount.google.com/apppasswords) — NOT their normal password, and NOT
    OAuth. This keeps the demo simple while still sending real emails from
    the student's own inbox. The app password is stored only in the
    in-memory demo store for this session and is never shown back to the
    frontend.
    """
    gmail_address: EmailStr
    app_password: str
