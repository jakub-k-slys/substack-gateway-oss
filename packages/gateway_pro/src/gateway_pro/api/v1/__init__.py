from fastapi import APIRouter

from gateway_pro.api.v1.drafts import router as drafts_router
from gateway_pro.api.v1.notes import router as notes_router
from gateway_pro.api.v1.posts import router as posts_router
from gateway_pro.api.v1.users import router as users_router

router = APIRouter()
router.include_router(drafts_router)
router.include_router(notes_router)
router.include_router(posts_router)
router.include_router(users_router)
