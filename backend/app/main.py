from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.router import router

settings = get_settings()

app = FastAPI(
    title="Signal API",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}
