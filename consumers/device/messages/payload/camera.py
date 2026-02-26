from pydantic import BaseModel


class CameraOffer(BaseModel):
    sdp: str
    type: str


class CameraOfferRequest(BaseModel):
    token: str
    rtsp: str
    offer: CameraOffer


class CameraOfferResponse(BaseModel):
    token: str
    answer: CameraOffer


class CameraAnswerResponse(BaseModel):
    token: str
    answer: CameraOffer


class CameraDisconnectPayload(BaseModel):
    pass


class CameraError(BaseModel):
    token: str
    error: str
