from pydantic import BaseModel


class PlaySequenceExtraSettings(BaseModel):
    pattern: list[int]
    repeat: int
