from fastapi import FastAPI
from .database import Base, engine
from app.endpoints.items_endpoints import router as items_router
from app.endpoints.item_pools_endpoints import router as items_pools_router
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(items_router)
app.include_router(items_pools_router)

if __name__ == "__main__":
    uvicorn.run(app)
