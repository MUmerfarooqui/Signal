from fastapi import APIRouter

from app.api.routes import briefs, connectors, orgs

router = APIRouter()

router.include_router(orgs.router, prefix="/orgs", tags=["orgs"])
router.include_router(connectors.router, prefix="/connectors", tags=["connectors"])
router.include_router(briefs.router, prefix="/briefs", tags=["briefs"])
