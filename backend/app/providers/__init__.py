"""
Provider factory. Everything else in the app calls get_data_provider() /
get_ai_provider() and never imports a concrete provider class directly —
this is what makes DATA_PROVIDER / AI_PROVIDER a one-line .env switch.
"""
from functools import lru_cache

from app.config import get_settings
from app.providers.base_provider import BaseDataProvider, BaseAIProvider


@lru_cache
def get_data_provider() -> BaseDataProvider:
    settings = get_settings()
    if settings.data_provider == "supabase":
        from app.providers.supabase_provider import SupabaseDataProvider
        return SupabaseDataProvider()
    from app.providers.demo_provider import DemoDataProvider
    return DemoDataProvider()


@lru_cache
def get_ai_provider() -> BaseAIProvider:
    settings = get_settings()
    if settings.ai_provider == "groq":
        from app.providers.groq_provider import GroqAIProvider
        return GroqAIProvider()
    from app.providers.demo_provider_ai import DemoAIProvider
    return DemoAIProvider()
