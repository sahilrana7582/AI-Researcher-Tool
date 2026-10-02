from fastapi import APIRouter

from app.api.v1.research import router as research_router

api_router = APIRouter()
api_router.include_router(research_router)
