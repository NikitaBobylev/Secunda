from pydantic import BaseModel, ConfigDict


class ActivityOut(BaseModel):
    id: int
    name: str
    level: int
    parent_id: int | None

    model_config = ConfigDict(from_attributes=True)
