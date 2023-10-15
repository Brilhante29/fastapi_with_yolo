from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from src.core.enums.media_types_enum import MediaTypes

from src.modules.yolov8.service import generate_video

templates = Jinja2Templates(directory="src/modules/yolov8/templates")

router = APIRouter(tags=['yolov8'])

@router.get("/video_feed/{source}")
async def video_feed(source):
    return StreamingResponse(generate_video(source), media_type=MediaTypes.VIDEO.value)


@router.get("/video")
async def video(request: Request):
    return templates.TemplateResponse("video_template.html", {"request": request})
