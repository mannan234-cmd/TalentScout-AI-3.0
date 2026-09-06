"""
Central app configuration. Everything is env-driven so switching between
demo mode and real backends (Supabase / Groq) never requires touching code.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "TalentScout AI 3.0"
    env: str = "development"
    secret_key: str = "change-this-secret-key-in-production"
    access_token_expire_minutes: int = 1440
    algorithm: str = "HS256"

    data_provider: str = "demo"   # demo | supabase
    ai_provider: str = "demo"     # demo | groq

    supabase_url: str = ""
    supabase_key: str = ""

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-70b-versatile"

    frontend_origin: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()
