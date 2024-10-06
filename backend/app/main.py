import uvicorn
from app.database import Base, engine
from app.endpoints.item_pools_endpoints import router as item_pools_router
from app.endpoints.items_endpoints import router as items_router
from app.endpoints.trinkets_endpoints import router as trinkets_router
from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(items_router)
    application.include_router(trinkets_router)
    application.include_router(item_pools_router)
    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app)
