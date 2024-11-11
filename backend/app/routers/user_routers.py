from app.endpoints.user_endpoints import router as users_router
from fastapi import APIRouter

user_router = APIRouter(prefix="/auth", tags=["User endpoints"])
user_router.include_router(users_router)
