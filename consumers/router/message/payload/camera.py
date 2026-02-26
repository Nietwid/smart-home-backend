from pydantic import BaseModel


class CameraRouterMessagePayload(BaseModel):
    id: int
    rtsp: str
