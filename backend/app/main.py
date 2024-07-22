from fastapi import FastAPI
from .database import Base, engine
from .endpoints.item import router as item_router
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(item_router)


if __name__ == "__main__":
    uvicorn.run(app)