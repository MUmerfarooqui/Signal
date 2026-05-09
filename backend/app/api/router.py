from fastapi import APIRouter

from app.api.routes import connectors

router = APIRouter()

router.include_router(connectors.router, prefix="/connectors", tags=["connectors"])
