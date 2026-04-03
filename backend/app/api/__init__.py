from fastapi import APIRouter
from app.api import opportunities

router = APIRouter()

router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
