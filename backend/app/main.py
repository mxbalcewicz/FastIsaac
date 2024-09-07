import uvicorn
from app.database import Base, engine
from app.endpoints.item_pools_endpoints import router as item_pools_router
from app.endpoints.items_endpoints import router as items_router
from app.endpoints.trinkets_endpoints import router as trinkets_router
from fastapi import FastAPI

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(items_router)
app.include_router(trinkets_router)
app.include_router(item_pools_router)


if __name__ == "__main__":
    uvicorn.run(app)
