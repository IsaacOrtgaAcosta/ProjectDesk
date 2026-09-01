from fastapi import FastAPI
from app.routers.projects import router


app = FastAPI()


app.include_router(router)
