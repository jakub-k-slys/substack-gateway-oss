from fastapi import APIRouter

from gateway_oss.api.v1.health import router as health_router
from gateway_oss.api.v1.me import router as me_router
from gateway_oss.api.v1.profiles import router as profiles_router

router = APIRouter()
router.include_router(health_router)
router.include_router(me_router)
router.include_router(profiles_router)
