from pydantic import BaseModel, Field
from app.schemas.geo import Latitude, Longitude

class AddressBase(BaseModel):
    label: str | None = None
    latitude: Latitude
    longitude: Longitude
    postal_code: str | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None
    district: str | None = None
    street: str | None = None

class AddressCreate(BaseModel):
    latitude: Latitude
    longitude: Longitude
    label: str | None = Field(default=None, min_length=1, max_length=120)

class AddressUpdate(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=120)
    latitude: Latitude | None = None
    longitude: Longitude | None = None
    postal_code: str | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None
    district: str | None = None
    street: str | None = None

class AddressOut(AddressBase):
    id: int
    class Config:
        from_attributes = True
