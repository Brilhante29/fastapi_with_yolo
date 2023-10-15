from fastapi import APIRouter
from src.modules.yolov8.controller import router as yolov8_router

api_router = APIRouter()
api_router.include_router(yolov8_router)