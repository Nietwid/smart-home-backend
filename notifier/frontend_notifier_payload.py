from pydantic import BaseModel


class AddTagResultPayload(BaseModel):
    status: int
    intent_id: str
    card_name: str
