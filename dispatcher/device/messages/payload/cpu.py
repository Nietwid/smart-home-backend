from pydantic import BaseModel


class UpdatePeripheralIntentPayload(BaseModel):
    peripheral_id: int
