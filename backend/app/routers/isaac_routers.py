from fastapi import APIRouter

isaac_router = APIRouter(prefix="/isaac", tags=["Isaac API endpoints"])

from app.endpoints import item_pools_endpoints, items_endpoints, trinkets_endpoints
