# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse, StreamingResponse
# from ultralytics import YOLO
# import cv2

# app = FastAPI()

# model = YOLO('yolov8n.pt')  # Carrega o modelo YOLO

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# def generate_video():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         results = model.track(frame, persist=True)  # Detecta objetos no frame
#         frame_ = results[0].plot()  # Plota os resultados

#         # Converta o frame em JPEG e envie-o
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame_)[1].tobytes() + b'\r\n')
#     cap.release()

# @app.get("/video_feed")
# async def video_feed():
#     return StreamingResponse(generate_video(), media_type="multipart/x-mixed-replace;boundary=frame")

# @app.get("/video")
# async def video():
#     html = """
#     <html>
#         <head>
#             <title>Video Streaming with YOLO</title>
#         </head>
#         <body>
#             <h1>Video Streaming with YOLO Detection</h1>
#             <img src="/video_feed">
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html, status_code=200)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from ultralytics import YOLO
import cv2

app = FastAPI()

model = YOLO('yolov8n.pt')  # Carrega o modelo YOLO

@app.get("/")
async def read_root():
    return {"Hello": "World"}

def generate_video():
    cap = cv2.VideoCapture('assets/test.mp4')
    if not cap.isOpened():
        raise Exception("Erro ao abrir o arquivo de vídeo")
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            break
        results = model.track(frame, persist=True)  # Detecta objetos no frame
        frame_ = results[0].plot()  # Plota os resultados

        # Converta o frame em JPEG e envie-o
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame_)[1].tobytes() + b'\r\n')

@app.get("/video_feed")
async def video_feed_endpoint():
    return StreamingResponse(generate_video(), media_type="multipart/x-mixed-replace;boundary=frame")

@app.get("/video")
async def video():
    html = """
    <html>
        <head>
            <title>Video Streaming with YOLO</title>
        </head>
        <body>
            <h1>Video Streaming with YOLO Detection</h1>
            <img src="/video_feed">
        </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)