import asyncio
import threading
import cv2
from ultralytics import YOLO
from src.core.enums.video_source_types_enum import VideoSourceType

MODEL_PATH = '../../ml/models/yolov8/yolov8n.pt'
MODEL_PATH_POSE = '../../ml/models/yolov8/yolov8n-pose.pt'
FRAME_STRING = (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n')

def setup_model():
    return YOLO(MODEL_PATH)


def setup_video_source(source: str):
    video_actions = {
        VideoSourceType.WEBCAM.value: lambda: cv2.VideoCapture(0),
        VideoSourceType.FILE.value: lambda: cv2.VideoCapture(source)
    }
    return video_actions.get(source, lambda: cv2.VideoCapture(source))()


async def generate_video(source: str):
    loop = asyncio.get_event_loop()
    model = YOLO(MODEL_PATH)
    cap = setup_video_source(source)

    if not cap.isOpened():
        cap.release()
        raise Exception("Erro ao abrir o arquivo de vídeo")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = await loop.run_in_executor(None, model.track, frame, True)
            results_list = list(results)  # Convert generator to list if necessary
            if results_list:
                frame_ = results_list[0].plot()
                yield FRAME_STRING + cv2.imencode('.jpg', frame_)[1].tobytes() + b'\r\n'
    finally:
        cap.release()
        
        

async def generate_video_pose(source: str):
    model = YOLO(MODEL_PATH_POSE)
    cap = setup_video_source(source)

    if not cap.isOpened():
        cap.release()
        raise Exception("Erro ao abrir o arquivo de vídeo")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)
            results_list = list(results)  # Convert generator to list if necessary
            if results_list:
                frame_ = results_list[0].plot()
                yield FRAME_STRING + cv2.imencode('.jpg', frame_)[1].tobytes() + b'\r\n'
    finally:
        cap.release()



