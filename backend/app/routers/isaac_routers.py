from app.endpoints.item_pools_endpoints import router as item_pools_router
from app.endpoints.items_endpoints import router as items_router
from app.endpoints.trinkets_endpoints import router as trinkets_router
from fastapi import APIRouter

isaac_router = APIRouter(prefix="/isaac", tags=["Isaac API endpoints"])
isaac_router.include_router(trinkets_router)
isaac_router.include_router(items_router)
isaac_router.include_router(item_pools_router)
