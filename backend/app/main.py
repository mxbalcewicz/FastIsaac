from fastapi import FastAPI
from .database import Base, engine
from .endpoints import router
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)