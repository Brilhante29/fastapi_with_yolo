from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from src.core.enums.media_types_enum import MediaTypes
from src.modules.yolov8.service import generate_video, generate_video_pose

templates = Jinja2Templates(directory="src/modules/yolov8/templates")
router = APIRouter(tags=['yolov8'])

@router.get("/video_feed/{source_type}/{source}")
async def video_feed(source_type: str, source: str):
    if source_type == 'normal':
        return StreamingResponse(generate_video(source), media_type=MediaTypes.VIDEO.value)
    elif source_type == 'pose':
        return StreamingResponse(generate_video_pose(source), media_type=MediaTypes.VIDEO.value)
    else:
        raise HTTPException(status_code=400, detail="Invalid source type")

@router.get("/video")
async def video(request: Request):
    return templates.TemplateResponse("video_template.html", {"request": request})
