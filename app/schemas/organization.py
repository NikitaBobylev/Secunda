from pydantic import BaseModel, ConfigDict

from app.schemas.activity import ActivityOut
from app.schemas.building import BuildingOut


class OrganizationPhoneOut(BaseModel):
    id: int
    phone: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationOut(BaseModel):
    id: int
    name: str
    building: BuildingOut
    phones: list[OrganizationPhoneOut]
    activities: list[ActivityOut]

    model_config = ConfigDict(from_attributes=True)
