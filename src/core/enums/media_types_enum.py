from enum import Enum

class MediaTypes(Enum):
    VIDEO = "multipart/x-mixed-replace;boundary=frame"
    IMAGE_JPEG = "image/jpeg"
    TEXT_HTML = "text/html"
    TEXT_PLAIN = "text/plain"
    IMAGE_PNG = "image/png"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"
    AUDIO_MPEG = "audio/mpeg"
    AUDIO_OGG = "audio/ogg"
    VIDEO_WEBM = "video/webm"