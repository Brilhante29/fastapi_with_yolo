from fastapi import FastAPI
from src.core.routes.api_router import api_router

app = FastAPI()

app.include_router(router=api_router)
