"""Håndtere routing for backend."""

from fastapi import APIRouter

from .delete import router as delete_router
from .get import router as get_router
from .post import router as post_router
from .put import router as put_router

router = APIRouter()

router.include_router(get_router)
router.include_router(delete_router)
router.include_router(post_router)
router.include_router(put_router)
