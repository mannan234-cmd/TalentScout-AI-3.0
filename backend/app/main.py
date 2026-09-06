from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.endpoints import router as api_router
from app.data.demo_data import seed_demo_data

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Intelligent, multi-agent student discovery & career-matching platform. "
        "AI agents provide advisory recommendations only; a human reviewer must "
        "explicitly approve a candidate before Matching & Application Support run."
    ),
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "app": settings.app_name, "data_provider": settings.data_provider, "ai_provider": settings.ai_provider}


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    if settings.data_provider == "demo":
        seed_demo_data()
