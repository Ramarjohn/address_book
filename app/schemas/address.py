from pydantic import BaseModel, Field
from app.schemas.geo import Latitude, Longitude

class AddressBase(BaseModel):
    label: str = Field(..., min_length=1, max_length=120)
    latitude: Latitude
    longitude: Longitude

class AddressCreate(AddressBase):
    label: str | None = Field(default=None, min_length=1, max_length=120)

class AddressUpdate(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=120)
    latitude: Latitude | None = None
    longitude: Longitude | None = None

class AddressOut(AddressBase):
    id: int
    class Config:
        from_attributes = True
