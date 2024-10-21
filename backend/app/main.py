import uvicorn
from app.routers.isaac_routers import isaac_router
from app.routers.user_routers import user_router
from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(isaac_router)
    application.include_router(user_router)
    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app)
