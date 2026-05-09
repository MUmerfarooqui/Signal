from fastapi import APIRouter

from app.api.routes import briefs, connectors, orgs, pulse

router = APIRouter()

router.include_router(orgs.router, prefix="/orgs", tags=["orgs"])
router.include_router(connectors.router, prefix="/connectors", tags=["connectors"])
router.include_router(briefs.router, prefix="/briefs", tags=["briefs"])
router.include_router(pulse.router, prefix="/pulse", tags=["pulse"])
