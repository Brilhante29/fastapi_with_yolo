from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO
import cv2
import threading
import asyncio

from src.core.enums.media_types_enum import MediaTypes

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

BASE_ML_PATH = 'src/core/ml/models/yolov8'

# Carregar modelos YOLO
track_model = YOLO(f'{BASE_ML_PATH}/yolov8n.pt')
face_model = YOLO(f'{BASE_ML_PATH}/yolov8n-face.pt')
pose_model = YOLO(f'{BASE_ML_PATH}/yolov8n-pose.pt')

frame_lock = threading.Lock()
current_frame = None
camera_is_on = False
cap = None

def capture_video():
    global camera_is_on, cap, current_frame
    camera_is_on = True
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    try:
        while camera_is_on:
            ret, frame = cap.read()
            if not ret:
                break
            with frame_lock:
                current_frame = frame.copy() if frame is not None else None
    finally:
        cap.release()

def ensure_camera_is_on():
    global camera_is_on
    if not camera_is_on:
        capture_thread = threading.Thread(target=capture_video)
        capture_thread.start()

async def stop_camera():
    global camera_is_on
    await asyncio.sleep(5)  # espera 5 segundos antes de desligar a câmera
    if camera_is_on:
        camera_is_on = False

def generate_video(model, mode: str, background_tasks: BackgroundTasks = None):
    ensure_camera_is_on()
    try:
        while True:
            with frame_lock:
                frame = current_frame.copy() if current_frame is not None else None
            if frame is None:
                continue
            if mode == 'tracking':
                results = model.track(frame, persist=True)
            elif mode == 'face':
                results = model.predict(frame)
            else:  # mode == 'pose'
                results = model(frame)
            frame_ = results[0].plot()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame_)[1].tobytes() + b'\r\n')
    finally:
        # Agende a câmera para ser desligada após um atraso, dando a outros endpoints a chance de mantê-la ligada, se necessário.
        if background_tasks:
            background_tasks.add_task(stop_camera)

@app.get("/video_feed_pose")
async def video_feed_endpoint(background_tasks: BackgroundTasks):
    return StreamingResponse(generate_video(pose_model, mode='pose', background_tasks=background_tasks), media_type=MediaTypes.VIDEO.value)

@app.get("/video_feed_face")
async def video_feed_face_endpoint(background_tasks: BackgroundTasks):
    return StreamingResponse(generate_video(face_model, mode='face', background_tasks=background_tasks), media_type=MediaTypes.VIDEO.value)

@app.get("/video_feed_track")
async def video_feed_track_endpoint(background_tasks: BackgroundTasks):
    return StreamingResponse(generate_video(track_model, mode='tracking', background_tasks=background_tasks), media_type=MediaTypes.VIDEO.value)
@app.get("/video")
async def video(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})

